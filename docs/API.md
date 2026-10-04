# API details

## Endpoint

`GET /frd/data/1.0/forecast`

The response includes `cod` (string), `cnt` (number of intervals), `list` (flat interval array), and `city`. A successful request uses HTTP 200. Each interval has a millisecond timestamp `dt` and a `main` object containing `temp`, `rain`, `humidity`, `wind_speed` and `sky`.

### Forecast intervals

| Day index | Original assumed resolution | Intervals per day |
| --- | --- | --- |
| 0–1 | 6 hours | 4 |
| 2–3 | 12 hours | 2 |
| 4–6 | Daily | 1 |

A full seven-day response therefore contains 15 intervals when the expected upstream data is available. For later days, temperature and humidity are approximated by the midpoint of daily minima and maxima; this is not a measured daily mean.

### Historical mode

With `history > 0`, `temp`, `humidity` and `wind_speed` become objects with:

- `current`: the forecast value for the interval.
- `previous`: one historical daily value per requested year.
- `diff`: current value minus the mean of `previous`, rounded to two decimals.

The same historical daily value is reused across that day's forecast intervals. `rain` and `sky` remain forecast-only values. The response also includes `years`, containing the current year and historical years selected by the date calculation.

### Interpretation and known limitations

- `rain` is **forecast probability of precipitation (%)**, not rainfall in millimetres. The client shows the arithmetic mean of interval probabilities; this is not a calibrated probability of rain over the whole day.
- `metric` leaves source wind values unchanged. Forecast `velocidad` and historical `velmedia` must be checked against their source units before comparison. The original client labels wind as m/s, and the `standard` conversion assumes m/s. These assumptions are retained and are not independently verified here. Wind charts and historical wind differences should not be used for decisions until units are harmonised.
- The coursework uses `standard` to mean Fahrenheit and an assumed m/s-to-mph wind conversion. It does not mean Kelvin or a general API standard.
- Historical selection subtracts 367 days initially, then 366 per additional year. It does not implement exact calendar-year alignment, and daily observations are matched by array index rather than date.
- Timestamps are generated from naive datetimes and therefore depend on the server's local timezone.
- AEMET may omit time intervals, values or historical fields. The positional parser does not yet accommodate every missing or changed field; malformed payloads can still lead to HTTP 500.
- The API has no authentication, cache, persistence, retry policy or public deployment setup. It binds to localhost, with Flask debug mode disabled.

### Error responses

| HTTP status | Situation |
| --- | --- |
| 400 | Invalid `q`, unsupported city/country/units, noninteger or out-of-range days/history |
| 502 | Upstream HTTP/network error or missing data URL |
| 503 | Missing server-side `AEMET_API_KEY` |

Individual upstream HTTP requests have a 20-second timeout. Historical mode makes multiple sequential requests and can therefore take longer than 20 seconds overall. Error messages do not echo upstream URLs containing the credential.
