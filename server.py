import os
from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

#La documentación de la API se encuentra en docs/API.md
#También indicar, que he redondeado a lo largo del código aquellos valores que al hacer pruebas observaba que tenían muchos decimales

def temp_a_standard(celsius): #Pasamos la temperatura de celsius a Fahrenheit
    return celsius * 9 / 5 + 32

def viento_a_standard(metros_por_segundo): #Pasamos la velocidad del viento a millas por hora
    return metros_por_segundo * 2.23694

def pasar_a_miliseg(fecha_hora): #Función para pasar una fecha y hora a milisegundos
    #Convertimos la cadena en un objeto datetime
    fecha_obj = datetime.strptime(fecha_hora, "%Y-%m-%d-%H")
    
    #Convertimos la fecha a milisegundos desde la época Unix
    milisegundos = int(fecha_obj.timestamp() * 1000)
    
    return milisegundos

def obtener_datos_actuales(prediccion, dia, units): #Función para obtener datos actuales
    #Lista vacía que almacenará los diccionarios con claves "dt" y "main"
    lista_diccionarios = list()
    #Condiciones en función del día que sea
    if dia in (0, 1):
        #Dato fecha que sigue esa distribución y la spliteamos por la T para quedarnos solo con la fecha
        fecha = prediccion[0]['prediccion']['dia'][dia]['fecha'].split('T')[0]
        #Bucle para ir de intervalo en intervalo(4 intervalos de 6 horas)
        for j in range (3, 7):
            #Hora inicio del intervalo para guardarla y despues pasar a ms junto con la fecha
            hora_inicio = prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][j]['periodo'].split('-')[0]
            fecha_hora = fecha + '-' + hora_inicio
            if units == "standard":
                lista_diccionarios.append({
                                        "dt": pasar_a_miliseg(fecha_hora),
                                        "main": {
                                                    "temp": temp_a_standard(prediccion[0]['prediccion']['dia'][dia]['temperatura']['dato'][j - 3]['value']),
                                                    "rain": prediccion[0]['prediccion']['dia'][dia]['probPrecipitacion'][j]['value'],
                                                    "humidity": prediccion[0]['prediccion']['dia'][dia]['humedadRelativa']['dato'][j - 3]['value'],
                                                    "wind_speed": round(viento_a_standard(prediccion[0]['prediccion']['dia'][dia]['viento'][j]['velocidad']), 2),
                                                    "sky": prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][j]['descripcion'],
                            }
                            })
            else:
                lista_diccionarios.append({
                                        "dt": pasar_a_miliseg(fecha_hora),
                                        "main": {
                                                    "temp": prediccion[0]['prediccion']['dia'][dia]['temperatura']['dato'][j - 3]['value'],
                                                    "rain": prediccion[0]['prediccion']['dia'][dia]['probPrecipitacion'][j]['value'],
                                                    "humidity": prediccion[0]['prediccion']['dia'][dia]['humedadRelativa']['dato'][j - 3]['value'],
                                                    "wind_speed": prediccion[0]['prediccion']['dia'][dia]['viento'][j]['velocidad'],
                                                    "sky": prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][j]['descripcion'],
                            }
                            })
                
               
        return lista_diccionarios
    #Mismo proceso con el resto de días, lo único que cambia es la distibución de algunos valores
    elif dia in (2,3):
            
        fecha = prediccion[0]['prediccion']['dia'][dia]['fecha'].split('T')[0]

        temp_max = prediccion[0]['prediccion']['dia'][dia]['temperatura']['maxima']
        temp_min = prediccion[0]['prediccion']['dia'][dia]['temperatura']['minima']
                    
        hum_max = prediccion[0]['prediccion']['dia'][dia]['humedadRelativa']['maxima']
        hum_min = prediccion[0]['prediccion']['dia'][dia]['humedadRelativa']['minima']

        for j in range (1, 3):
               
            hora_inicio = prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][j]['periodo'].split('-')[0]
            fecha_hora = fecha + '-' + hora_inicio
            if units == "standard":
                lista_diccionarios.append({
                                        "dt": pasar_a_miliseg(fecha_hora),
                                        "main": {
                                                    "temp": temp_a_standard(((temp_max) + (temp_min))/2),
                                                    "rain": prediccion[0]['prediccion']['dia'][dia]['probPrecipitacion'][j]['value'],
                                                    "humidity": ((hum_max) + (hum_min)) / 2,
                                                    "wind_speed": round(viento_a_standard(prediccion[0]['prediccion']['dia'][dia]['viento'][j]['velocidad']), 2),
                                                    "sky": prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][j]['descripcion']
                            }
                            })
            else:
                lista_diccionarios.append({
                                        "dt": pasar_a_miliseg(fecha_hora),
                                        "main": {
                                                    "temp": ((temp_max) + (temp_min))/2,
                                                    "rain": prediccion[0]['prediccion']['dia'][dia]['probPrecipitacion'][j]['value'],
                                                    "humidity": ((hum_max) + (hum_min)) / 2,
                                                    "wind_speed": prediccion[0]['prediccion']['dia'][dia]['viento'][j]['velocidad'],
                                                    "sky": prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][j]['descripcion']
                            }
                            })
        return lista_diccionarios

    elif dia in (4,5,6):

        temp_max = prediccion[0]['prediccion']['dia'][dia]['temperatura']['maxima']
        temp_min = prediccion[0]['prediccion']['dia'][dia]['temperatura']['minima']
                    
        hum_max = prediccion[0]['prediccion']['dia'][dia]['humedadRelativa']['maxima']
        hum_min = prediccion[0]['prediccion']['dia'][dia]['humedadRelativa']['minima']

        fecha = prediccion[0]['prediccion']['dia'][dia]['fecha'].split('T')[0]
        hora_inicio = '00'
        fecha_hora = fecha + '-' + hora_inicio
        if units == "standard":
            lista_diccionarios.append({
                                        "dt": pasar_a_miliseg(fecha_hora),
                                        "main": {
                                                    "temp": temp_a_standard(((temp_max) + (temp_min))/2),
                                                    "rain": prediccion[0]['prediccion']['dia'][dia]['probPrecipitacion'][0]['value'],
                                                    "humidity": ((hum_max) + (hum_min)) / 2,
                                                    "wind_speed": round(viento_a_standard(prediccion[0]['prediccion']['dia'][dia]['viento'][0]['velocidad']), 2),
                                                    "sky": prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][0]['descripcion']
                            }
                            })
        else:
            lista_diccionarios.append({
                                        "dt": pasar_a_miliseg(fecha_hora),
                                        "main": {
                                                    "temp": ((temp_max) + (temp_min))/2,
                                                    "rain": prediccion[0]['prediccion']['dia'][dia]['probPrecipitacion'][0]['value'],
                                                    "humidity": ((hum_max) + (hum_min)) / 2,
                                                    "wind_speed": prediccion[0]['prediccion']['dia'][dia]['viento'][0]['velocidad'],
                                                    "sky": prediccion[0]['prediccion']['dia'][dia]['estadoCielo'][0]['descripcion']
                            }
                            })
        
        return lista_diccionarios

def media(l_valores): #Función para hacer la media de  una lista de valores
    return sum(l_valores) / len(l_valores) if l_valores else 0  #Manejo de lista vacía, aunque en estos caso nunca va a haber una lista vacía

def convertir_a_float(valor):#Función para convertir los valores climatológicos de previsiones pasadas, a float
    #Reemplazamos la coma por un punto y convertimos a float
     return float(valor.strip().replace(",", "."))

def obtener_datos_historicos(prediccion_actual, predicciones_pasadas, dia, units, history):#Función para obtener datos históricos
    #Obtenemos los datos actuales del día dado usando la función definida
    lista_actual = obtener_datos_actuales(prediccion_actual, dia, units)
    
    #Listas vacías que almacenarán los valores históricos correspondientes
    l_temp_pasado, l_viento_pasado, l_hum_pasado = [],[],[]
    #Bucle para que itere tantas veces como años se hayan pasado a history
    for i in range(history):
        
        if units == "standard":
            temp_pasado = round(temp_a_standard(convertir_a_float((predicciones_pasadas[i])[dia]['tmed'])),2)# Temperatura histórica
            hum_pasado = convertir_a_float(predicciones_pasadas[i][dia]['hrMedia'])#Humedad histórica
            viento_pasado = round(viento_a_standard(convertir_a_float(predicciones_pasadas[i][dia]['velmedia'])), 2)#Velocidad del viento histórica
        
        else:
            temp_pasado = convertir_a_float((predicciones_pasadas[i])[dia]['tmed'])#Temperatura media histórica
            hum_pasado = convertir_a_float(predicciones_pasadas[i][dia]['hrMedia'])#Humedad histórica
            viento_pasado = convertir_a_float(predicciones_pasadas[i][dia]['velmedia'])#Velocidad del viento histórica

        #Voy añadiendo cada valor a su lista correspondiente
        l_temp_pasado.append(temp_pasado)
        l_hum_pasado.append(hum_pasado)
        l_viento_pasado.append(viento_pasado)
    #Hago la media de los valores de cada lista
    media_temp_pasado = media(l_temp_pasado)
    media_hum_pasado = media(l_hum_pasado)
    media_viento_pasado = media(l_viento_pasado)
    #Al observar como se distribuyen los datos, itero por cada diccionario en la lista de diccionarios
    for diccionario in lista_actual:
        #Itero por cada clave en las claves del diccionario
        for clave in diccionario.keys():
            #Si la clave es main, obtengo su valor, que es otro diccionario con los valores climatológicos
            if clave == "main":
                datos_clima = diccionario['main']
                #Itero sobre las claves del diccionario, y cuando detecte que son esas, las modifica
                for clave1 in datos_clima.keys():
                    if clave1 == "temp":
                        datos_clima['temp'] = {
                            "current": datos_clima['temp'],
                            "previous": l_temp_pasado,
                            "diff": round((datos_clima['temp'] - media_temp_pasado),2)
                        }

                    if clave1 == "humidity":
                        datos_clima['humidity'] = {
                            "current": datos_clima['humidity'],
                            "previous": l_hum_pasado,
                            "diff": round((datos_clima['humidity'] - media_hum_pasado), 2)
                        }
                    if clave1 == "wind_speed":
                        datos_clima['wind_speed'] = {
                            "current": datos_clima['wind_speed'],
                            "previous": l_viento_pasado,
                            "diff": round((datos_clima['wind_speed'] - media_viento_pasado), 2)
                        }
#Devuelve los datos actualizados con históricos integrados
    return lista_actual

app = Flask(__name__)

class AemetError(Exception):
    """The upstream service did not return a usable response."""


def get_aemet(url, **kwargs):
    if not url:
        raise AemetError()
    try:
        response = requests.get(url, timeout=20, **kwargs)
        response.raise_for_status()
        return response
    except requests.RequestException:
        # Never echo request URLs: upstream requests contain a credential.
        raise AemetError() from None


@app.errorhandler(AemetError)
def upstream_error(error):
    return jsonify({"error": "No se pudo consultar AEMET"}), 502


@app.route('/frd/data/1.0/forecast')
def forecast():#Función de mi servidor
    # Validate the public query before contacting AEMET.
    q = request.args.get('q', '')
    parts = q.split(',')
    if len(parts) != 2:
        return jsonify({"error": "q debe tener el formato ciudad,ES"}), 400
    ciudad, pais = parts[0].strip().lower(), parts[1].strip().upper()
    if ciudad not in {"murcia", "orihuela", "caravaca", "san javier"} or pais != "ES":
        return jsonify({"error": "Municipio o país no disponible"}), 400
    units = request.args.get('units', 'metric')
    if units not in {'metric', 'standard'}:
        return jsonify({"error": "units debe ser metric o standard"}), 400
    try:
        dias = int(request.args.get('d', '7'))
        history = int(request.args.get('history', '0'))
    except ValueError:
        return jsonify({"error": "d e history deben ser números enteros"}), 400
    if not 1 <= dias <= 7 or not 0 <= history <= 5:
        return jsonify({"error": "d debe estar entre 1 y 7; history entre 0 y 5"}), 400
    if not os.environ.get('AEMET_API_KEY'):
        return jsonify({"error": "Configura AEMET_API_KEY en el servidor"}), 503

    #Diccionarios con los municipios disponibles en nuestro servidor
    codigos = {"murcia": "30030", "orihuela": "03099", "caravaca": "30015", "san javier": "30035"}
    idemas = {"murcia": "7178I", "orihuela": "7244X", "caravaca": "7119B", "san javier": "7031X"}

    #Llamada a la API de AEMET, para predicciones actuales
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigos[ciudad]}"
    querystring = {"api_key": os.environ["AEMET_API_KEY"]}
    headers = {'cache-control': "no-cache"}
    response = get_aemet(url, headers=headers, params=querystring)

    #Obtenemos predicción actual
    if response.status_code == 200:
        datos = response.json()
        url_datos = datos.get("datos")
        response_datos = get_aemet(url_datos, headers=headers)
        if response_datos.status_code == 200:
            prediccion_actual = response_datos.json()
    
    #Fechas para la llamada a la API de AEMET de valores climatológicos anteriores
    fecha_actual = datetime.utcnow()
    fecha_inicio = fecha_actual - timedelta(days=367)
    fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%dT%H:%M:%SUTC')
    fecha_fin = fecha_inicio + timedelta(days=dias)
    fecha_fin_str = fecha_fin.strftime('%Y-%m-%dT%H:%M:%SUTC')

    #Lista para almacenar los diccionarios con claves "dt" y "main"
    lista = []
    #Lista para almacenar los años en caso de que se pase el parámetro history
    años = []
    #Lista que almacena las distintas predicciones del pasado
    predicciones_pasado = []
    #Obtenemos datos históricos si history es mayor que 0
    if history > 0:
        años = [fecha_actual.year]
        for _ in range(history):
            url1 = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_inicio_str}/fechafin/{fecha_fin_str}/estacion/{idemas[ciudad]}"
            response1 = get_aemet(url1, headers=headers, params=querystring)
            
            if response1.status_code == 200:
                datos1 = response1.json()
                url_datos1 = datos1.get("datos")
                response_datos1 = get_aemet(url_datos1, headers=headers)
                
                if response_datos1.status_code == 200:
                    
                    prediccion_pasado = response_datos1.json()
                    predicciones_pasado.append(prediccion_pasado)
                
                #Actualización de fechas para el año anterior
                años.append(fecha_inicio.year)
                fecha_inicio -= timedelta(days=366)#A partir de ahora resto 366 dias en vez de 367, porque ya no son bisiestos, aunque es verdad que a partir de otros cuatro años volverán a ser bisiestos
                fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%dT%H:%M:%SUTC')
                fecha_fin -= timedelta(days=366)
                fecha_fin_str = fecha_fin.strftime('%Y-%m-%dT%H:%M:%SUTC')
        #Para cada dia, obtengo su prediccion y la añado a la lista, mediante la concatenacion me aseguro de que el formato final sea igual al del enunciado, de esta forma seria una lista de diccionarios
        #y no una lista de listas de diccionarios, que sería en el caso de que hiciera append 
        for dia in range(dias):
            lista_auxiliar = (obtener_datos_historicos(prediccion_actual, predicciones_pasado, dia, units, history))
            lista += lista_auxiliar
        #Respuesta final, donde incluyo la lista years, ya que accedo a históricos        
        respuesta = {"cod": "200", "cnt": len(lista), "list": lista, "city": {"name": ciudad, "country": pais}, "years": años}
    
    else:
        #Mismo proceso que antes pero esta vez sin acceder a datos previos
        for i in range(dias):
            
            lista_auxiliar = obtener_datos_actuales(prediccion_actual, i, units)
            lista += lista_auxiliar
            
        respuesta = {"cod": "200", "cnt": len(lista), "list": lista, "city": {"name": ciudad, "country": pais}}

    #Respuesta final JSON
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')