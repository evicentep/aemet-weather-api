import requests
import matplotlib.pyplot as plt

print("¡Bienvenid@ a la previsión meteorológica de nuestras pistas de pádel exteriores!\n")

idemas = {"murcia": "7178I", "orihuela": "7244X", "caravaca": "7119B", "san javier": "7031X"}
codigos = {"murcia": "30030", "orihuela": "03099", "caravaca": "30015", "san javier": "30035"}

print("Los municipios en los que disponemos actualmente de pistas de pádel son:\n")
for clave in codigos.keys():
    print("- ", clave, "\n")

municipio = str(input("Introduce el nombre de la ciudad: ")).lower()

while municipio not in idemas.keys():
    print("Municipio no válido\n")
    municipio = str(input("Introduce el nombre de la ciudad: ")).lower()

dias = int(input("¿De cuántos días te gustaría saber la previsión?(El máximo de días son 7): "))

while dias not in range(1, 8):
    print("Número de días no válido\n")
    dias = int(input("Introduce una cantidad de días válida: "))

url = "http://127.0.0.1:5000/frd/data/1.0/forecast"
querystring = {"q": municipio + ",ES", "d": dias}
#En esta situcación acceder a valores pasados/históricos no tiene sentido, por lo que no incluyo el parámetro history,
#y el parámetro units tampoco es necesario, ya que como las pistas se enuentran es España, la unidad de medida va a ser metric
headers = {'cache-control': "no-cache"}
response = requests.request("GET", url, headers=headers, params=querystring, timeout=60)

if response.status_code == 200:
    prediccion = response.json()
    indice_global = 0  #Índice global para recorrer la lista de datos climáticos
    lluvia_dia = []
    viento_dia = []

    for i in range(dias):
        #Definimos el número de intervalos para cada día
        if i < 2:  #Día 1 y Día 2 - 4 intervalos
            intervalos = 4
        elif i < 4:  #Día 3 y Día 4 - 2 intervalos
            intervalos = 2
        else:  #Días 5, 6 y 7 - 1 intervalo
            intervalos = 1

        lluvia_intervalos = []
        viento_intervalos = []

        for j in range(intervalos):
            if indice_global < len(prediccion["list"]):
                #Extraemps los datos de lluvia y viento del JSON
                lluvia_intervalos.append(prediccion["list"][indice_global]["main"]["rain"])
                viento_intervalos.append(prediccion["list"][indice_global]["main"]["wind_speed"])
                indice_global += 1
            else:
                break

        #Calculamos los promedios y los almaceno en las listas principales
        if lluvia_intervalos:
            lluvia_promedio = sum(lluvia_intervalos) / len(lluvia_intervalos)
            lluvia_dia.append(lluvia_promedio)
        if viento_intervalos:
            viento_promedio = sum(viento_intervalos) / len(viento_intervalos)
            viento_dia.append(viento_promedio)

    #Mosramos los resultados
    print("\nProbabilidad media de precipitación diaria:", lluvia_dia)
    print("Velocidad del viento media diaria:", viento_dia)

    #Función para graficar
    def mostrar_grafico_actual(x_labels, datos, tipo):
        plt.figure(figsize=(10, 6))
        plt.bar(x_labels, datos, color='skyblue', width=0.5, align="center")
        plt.xlabel("Días")
        plt.ylabel(tipo)
        plt.title(f"{tipo} por día en los próximos {len(datos)} días")
        plt.show()

    #Menú de selección
    dias_semana = [f'Día {i + 1}' for i in range(dias)]
    opcion = input("\nEntre los siguientes datos:\n1- Precipitación\n2- Velocidad del viento\n3- Fin del programa\n"
                   "Introduce 1, 2 o 3 según la opción que más desees: ")

    while opcion not in ("1", "2", "3"):
        opcion = input("Introduce una opción correcta: ")

    while opcion != "3":
        if opcion == "1":  #Opción de Precipitación
            print("\n       Probabilidad media de precipitación diaria\n")
            for i in range(dias):
                print(f"Día {i + 1}: {lluvia_dia[i]} %")
            mostrar_grafico_actual(dias_semana, lluvia_dia, "Probabilidad media de precipitación (%)")

        elif opcion == "2":  # Opción de Velocidad del Viento
            print("\n       Velocidad media del viento diaria\n")
            for i in range(dias):
                print(f"Día {i + 1}: {viento_dia[i]} m/s")
            mostrar_grafico_actual(dias_semana, viento_dia, "Velocidad del Viento Media m/s")

        opcion = input("Introduce otra opción si lo deseas: ")
        while opcion not in ("1", "2", "3"):
            opcion = input("Introduce una opción correcta: ")

    print("Fin del programa")
else:
    print("Error en la conexión con el servidor.")
