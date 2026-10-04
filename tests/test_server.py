"""Offline regression checks; fixtures are synthetic, not live AEMET data."""
import os
import unittest
from unittest.mock import Mock, patch

import requests
import server


def forecast_fixture():
    days = []
    for i in range(7):
        periods = ['00-24', '00-12', '12-24', '00-06', '06-12', '12-18', '18-24']
        days.append({
            'fecha': f'2025-01-{i + 1:02d}T00:00:00',
            'estadoCielo': [{'periodo': p, 'descripcion': 'Despejado'} for p in periods],
            'temperatura': {'dato': [{'value': 20}] * 4, 'minima': 10, 'maxima': 30},
            'humedadRelativa': {'dato': [{'value': 60}] * 4, 'minima': 40, 'maxima': 80},
            'probPrecipitacion': [{'value': 25}] * 7,
            'viento': [{'velocidad': 10}] * 7,
        })
    return [{'prediccion': {'dia': days}}]


def response(data):
    item = Mock(status_code=200)
    item.json.return_value = data
    return item


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.client = server.app.test_client()
        self.environment = patch.dict(os.environ, {'AEMET_API_KEY': 'offline-test-key'})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    @patch('server.requests.get')
    def test_invalid_queries_never_contact_upstream(self, upstream):
        for query in ['', 'q=murcia', 'q=unknown,ES', 'q=murcia,FR',
                      'q=murcia,ES&d=0', 'q=murcia,ES&d=8',
                      'q=murcia,ES&d=abc', 'q=murcia,ES&history=-1',
                      'q=murcia,ES&history=6', 'q=murcia,ES&units=other']:
            with self.subTest(query=query):
                self.assertEqual(self.client.get('/frd/data/1.0/forecast?' + query).status_code, 400)
        upstream.assert_not_called()

    @patch('server.requests.get')
    def test_seven_day_forecast_and_server_side_key(self, upstream):
        upstream.side_effect = [response({'datos': 'https://example.invalid/forecast'}), response(forecast_fixture())]
        result = self.client.get('/frd/data/1.0/forecast?q=Murcia,ES&d=7')
        self.assertEqual(result.status_code, 200)
        body = result.get_json()
        self.assertEqual(body['cnt'], 15)
        self.assertNotIn('years', body)
        self.assertEqual(body['list'][0]['main']['rain'], 25)
        self.assertEqual(upstream.call_args_list[0].kwargs['params']['api_key'], 'offline-test-key')
        self.assertEqual(upstream.call_args_list[0].kwargs['timeout'], 20)

    @patch('server.requests.get')
    def test_history_response(self, upstream):
        historical = [{'tmed': '18,0', 'hrMedia': '50', 'velmedia': '8'}]
        upstream.side_effect = [response({'datos': 'https://example.invalid/forecast'}), response(forecast_fixture()),
                                response({'datos': 'https://example.invalid/history'}), response(historical)]
        result = self.client.get('/frd/data/1.0/forecast?q=murcia,ES&d=1&history=1')
        self.assertEqual(result.status_code, 200)
        body = result.get_json()
        self.assertEqual(len(body['years']), 2)
        self.assertEqual(body['cnt'], 4)
        self.assertEqual(body['list'][0]['main']['temp'], {'current': 20, 'previous': [18.0], 'diff': 2.0})

    @patch('server.requests.get')
    def test_missing_key(self, upstream):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(self.client.get('/frd/data/1.0/forecast?q=murcia,ES').status_code, 503)
        upstream.assert_not_called()

    @patch('server.requests.get', side_effect=requests.Timeout('credential-must-not-appear'))
    def test_network_failure_does_not_leak_details(self, upstream):
        result = self.client.get('/frd/data/1.0/forecast?q=murcia,ES')
        self.assertEqual(result.status_code, 502)
        self.assertNotIn('credential-must-not-appear', result.get_data(as_text=True))

    @patch('server.requests.get')
    def test_missing_data_url(self, upstream):
        upstream.return_value = response({'estado': 429})
        self.assertEqual(self.client.get('/frd/data/1.0/forecast?q=murcia,ES').status_code, 502)


if __name__ == '__main__':
    unittest.main()
