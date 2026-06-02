import math
import matplotlib.pyplot as plt
from airport import IsSchengenAirport, LoadAirports


# FUNCIÓN 1
class Aircraft:
   def __init__(self, aircraft_id, company, origin, landing_time, destination, departure_time):
       self.id = aircraft_id
       self.company = company
       self.origin = origin
       self.time_of_landing = landing_time
       self.destination = destination
       self.departure_time = departure_time
       self.airline_icao = company
       prefijos_schengen = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV',
                            'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
       if len(origin) >= 2 and origin[:2] in prefijos_schengen:
           self.flight_type = "Schengen"
       else:
           self.flight_type = "non-Schengen"




def LoadArrivals(filename):
   arrivals = []
   try:
       file = open(filename, 'r')
   except FileNotFoundError:
       return arrivals
   lines = file.readlines()
   file.close()
   if len(lines) <= 1:
       return arrivals
   i = 1
   line = lines[i]
   while i < len(lines) and line != '':
       parts = line.split()
       if len(parts) == 4:
           aircraft_id = parts[0]
           origin = parts[1]
           time_str = parts[2]
           company = parts[3]
           if len(origin) == 4 and len(company) == 3 and len(time_str) == 5:
               if time_str[2] == ':':
                   digitos_validos = True
                   posicion = 0
                   while posicion < 5 and digitos_validos:
                       if posicion != 2:
                           caracter = time_str[posicion]
                           if not ('0' <= caracter <= '9'):
                               digitos_validos = False
                       posicion = posicion + 1
                   if digitos_validos:
                       hour_str = time_str[0] + time_str[1]
                       minute_str = time_str[3] + time_str[4]
                       hour = int(hour_str)
                       minute = int(minute_str)
                       if 0 <= hour <= 23 and 0 <= minute <= 59:
                           nuevo_vuelo = Aircraft(aircraft_id, company, origin, time_str, "", "")
                           arrivals.append(nuevo_vuelo)
       i = i + 1
       if i < len(lines):
           line = lines[i]
   return arrivals




# FUNCIÓN 2
def PlotArrivals(aircrafts):
   if not aircrafts:
       print("Error: la lista de aircraft está vacía")
       return
   frecuencias = [0] * 24
   i = 0
   for i in aircrafts:
       try:
           hora = int(i.time_of_landing.split(":")[0])
           if 0 <= hora <= 23:
               frecuencias[hora] += 1
       except (ValueError, AttributeError, IndexError):
           continue
   horas = list(range(24))
   plt.figure(figsize=(10, 5))
   plt.bar(horas, frecuencias, color='royalblue', edgecolor='black')
   plt.xlabel("Hora del día")
   plt.ylabel("Número de llegadas")
   plt.title("Frecuencia de llegadas por hora")
   plt.xticks(horas)
   plt.grid(axis='y', linestyle='--', alpha=0.7)
   plt.show()




# FUNCIÓN 3
def SaveFlights(aircrafts, filename):
   if not aircrafts:
       print("Error: La lista de aeronaves está vacía. No se ha creado ningún archivo.")
       return -1
   try:
       with open(filename, 'w') as f:
           f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
           i = 0
           for i in aircrafts:
               aid = i.id if i.id else "-"
               origin = i.origin if i.origin else "-"
               arrival = i.time_of_landing if i.time_of_landing else "-"
               airline = i.company if i.company else "-"
               f.write(f"{aid} {airline} {arrival} {origin}\n")
       print(f"Archivo '{filename}' guardado correctamente.")
   except FileNotFoundError:
       print("No existe el fichero")
   except ValueError:
       print("Datos incorrectos")
   except IndexError:
       print("Lista no encontrada")




# FUNCIÓN 4
def PlotAirlines(aircrafts):
   if len(aircrafts) == 0:
       print("La lista de vuelos esta vacía y no se puede mostrar el gráfico.")
       return
   companies = []
   frequencies = []
   i = 0
   while i < len(aircrafts):
       current_company = aircrafts[i].company
       found = False
       j = 0
       while j < len(companies) and not found:
           if companies[j] == current_company:
               frequencies[j] = frequencies[j] + 1
               found = True
           j = j + 1
       if not found:
           companies.append(current_company)
           frequencies.append(1)
       i = i + 1
   plt.bar(companies, frequencies)
   plt.title("Número de vuelos por aerolinea")
   plt.xlabel("Aerolinea (ICAO)")
   plt.ylabel("Cantidad de vuelos")
   plt.xticks(rotation=90, fontsize=5)
   plt.show()




# FUNCIÓN 5
def PlotFlightsType(aircrafts):
   if len(aircrafts) == 0:
       print("La lista de vuelos esta vacia y no se puede mostrar el grafico.")
       return
   prefijos_schengen = ['LE', 'LF', 'ED', 'EB', 'EH', 'LI', 'LS', 'LO', 'LK', 'LZ', 'LD', 'LG', 'LP', 'LR', 'LU', 'LW',
                        'LY', 'LA', 'LB', 'LC', 'LJ', 'LM', 'LN', 'LV', 'LX', 'EP', 'ES', 'ET', 'EV', 'EY', 'BI', 'BK',
                        'EN', 'GC', 'GM', 'DA', 'DT', 'DR', 'DX', 'DI', 'OE', 'OJ', 'OS', 'LT', 'LQ', 'UB', 'UD', 'UG',
                        'UK', 'UM', 'UT', 'UA', 'UU', 'UW', 'UY', 'UR', 'UL', 'UN', 'UI', 'UH', 'UE', 'UF', 'US']
   contador_schengen = 0
   contador_no_schengen = 0
   i = 0
   while i < len(aircrafts):
       origin = aircrafts[i].origin
       prefijo = origin[0] + origin[1]
       si_schengen = False
       j = 0
       while j < len(prefijos_schengen) and not si_schengen:
           if prefijos_schengen[j] == prefijo:
               si_schengen = True
           j = j + 1
       if si_schengen:
           contador_schengen = contador_schengen + 1
       else:
           contador_no_schengen = contador_no_schengen + 1
       i = i + 1
   categoria_unica_ejeX = ['Vuelos']
   valor_schengen = [contador_schengen]
   valor_no_schengen = [contador_no_schengen]
   plt.bar(categoria_unica_ejeX, valor_schengen, label='Schengen')
   plt.bar(categoria_unica_ejeX, valor_no_schengen, bottom=valor_schengen, label='No Schengen')
   plt.title("Vuelos desde paises Schengen y no Schengen")
   plt.ylabel("Cantidad de vuelos")
   plt.legend()
   plt.show()




# FUNCIÓN 6
def MapFlights(aircrafts):
   latitud_LEBL = 41.2971
   longitud_LEBL = 2.0785
   k = open("Aircrafts.kml", "w")
   k.write('<?xml version="1.0" encoding="UTF-8"?>\n')
   k.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
   k.write('<Document>\n')
   lista_aero = LoadAirports("Airports.txt")
   for flight in aircrafts:
       encontrado = False
       origen_latitud = 0
       origen_longitud = 0
       for a in lista_aero:
           if a.ICAOcode == flight.origin:
               origen_latitud = a.latitude
               origen_longitud = a.longitude
               encontrado = True
               break
       if encontrado:
           if IsSchengenAirport(flight.origin):
               color = "ff0000ff"
           else:
               color = "ff00ff00"
           k.write("<Placemark>")
           k.write(f'<name>Flight {flight.id}</name>\n')
           k.write('<Style>\n')
           k.write('<LineStyle>\n')
           k.write(f'<color>{color}</color>\n')
           k.write('<width>2</width>\n')
           k.write('</LineStyle>\n')
           k.write('</Style>\n')
           k.write('<LineString>\n')
           k.write('<coordinates>\n')
           k.write(f'{origen_longitud},{origen_latitud},0 {longitud_LEBL},{latitud_LEBL},0')
           k.write('\n</coordinates>\n')
           k.write('</LineString>\n')
           k.write('</Placemark>\n')
   k.write('</Document>\n')
   k.write('</kml>\n')
   k.close()




# FUNCIÓN 7
def Haversine3(lat1, lon1, lat2, lon2):
   R_tierra = 6371
   rad_lat1 = math.radians(lat1)
   rad_lat2 = math.radians(lat2)
   rad_lon1 = math.radians(lon1)
   rad_lon2 = math.radians(lon2)
   dphi = math.radians(lat2 - lat1)
   dlambda = math.radians(lon2 - lon1)
   a = math.sin(dphi / 2) ** 2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(dlambda / 2) ** 2
   b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
   return R_tierra * b




def LongDistanceArrivals(aircrafts):
   latitud_LEBL = 41.2971
   longitud_LEBL = 2.0785
   lista_aero = LoadAirports("Airports.txt")
   long_distance_flights = []
   for flight in aircrafts:
       encontrado = False
       origen_latitud = 0
       origen_longitud = 0
       for a in lista_aero:
           if a.ICAOcode == flight.origin:
               origen_latitud = a.latitude
               origen_longitud = a.longitude
               encontrado = True
               break
       if encontrado:
           distancia = Haversine3(origen_latitud, origen_longitud, latitud_LEBL, longitud_LEBL)
           if distancia > 2000:
               long_distance_flights.append(flight)
   return long_distance_flights




# version 4 funcion 1
def LoadDepartures(filename):
   departures = []
   try:
       file = open(filename, "r")
   except FileNotFoundError:
       return [], -1
   lines = file.readlines()
   file.close()
   if len(lines) <= 1:
       return departures
   i = 1
   while i < len(lines):
       line = lines[i]
       parts = line.split()
       if len(parts) != 4:
           print("Error en los datos del archivo")
       else:
           aircraft_id = parts[0]
           destination = parts[1]
           departure_time = parts[2]
           company = parts[3]
           nuevo = Aircraft(aircraft_id, company, "", "", destination, departure_time)
           departures.append(nuevo)
       i = i + 1
   return departures




# version 4 FUNCIÓN 2
def MergeMovements(arrivals, departures):
   if len(arrivals) == 0 or len(departures) == 0:
       return -1
   merged = []
   used_departures = []
   i = 0
   while i < len(arrivals):
       arr = arrivals[i]
       found = False
       j = 0
       while j < len(departures) and not found:
           dep = departures[j]
           if arr.id == dep.id:
               partes_landing = arr.time_of_landing.split(":")
               hora_landing = int(partes_landing[0])
               minutos_landing = int(partes_landing[1])
               total_landing = hora_landing * 60 + minutos_landing


               partes_departure = dep.departure_time.split(":")
               hora_departure = int(partes_departure[0])
               minutos_departure = int(partes_departure[1])
               total_departure = hora_departure * 60 + minutos_departure


               if total_landing < total_departure:
                   nuevo = Aircraft(arr.id, arr.company, arr.origin, arr.time_of_landing, dep.destination,
                                    dep.departure_time)
                   merged.append(nuevo)
                   used_departures.append(j)
                   found = True
           j = j + 1


       if not found:
           nuevo = Aircraft(arr.id, arr.company, arr.origin, arr.time_of_landing, "", "")
           merged.append(nuevo)
       i = i + 1


   j = 0
   while j < len(departures):
       if j not in used_departures:
           dep = departures[j]
           nuevo = Aircraft(dep.id, dep.company, "", "", dep.destination, dep.departure_time)
           merged.append(nuevo)
       j = j + 1
   return merged




# version 4 FUNCIÓN 3
# version 4 FUNCIÓN 3 (Modificada para leer desde MergedFlights.txt)
def NightAircraft(aircrafts):
   if len(aircrafts) == 0:
       return -1
   lista_nocturnos = []
   i = 0
   while i < len(aircrafts):
       a = aircrafts[i]
       # Vuelos sin información de llegada (nocturnos / solo salida)
       if a.origin == "" and a.time_of_landing == "":
           lista_nocturnos.append(a)
       i = i + 1
   return lista_nocturnos




# NUEVA FUNCIÓN PARA GUARDAR EL ARCHIVO DE VUELOS SIN LLEGADA
def SaveNightFlights(aircrafts, filename):
   if not aircrafts or aircrafts == -1:
       print("Error: La lista de vuelos está vacía o es inválida.")
       return -1


   try:
       with open(filename, 'w') as f:
           # Mantenemos el formato de cabecera
           f.write("ID AIRLINE ORIGIN ARRIVAL DESTINATION DEPARTURE\n")


           for a in aircrafts:
               aid = a.id if a.id else "-"
               airline = a.company if a.company else "-"
               # Como sabemos que no tienen origen ni llegada, ponemos guiones fijos
               origin = "-"
               arrival = "-"
               dest = a.destination if a.destination else "-"
               dep = a.departure_time if a.departure_time else "-"


               # Escribimos con un solo espacio de separación
               f.write(f"{aid} {airline} {origin} {arrival} {dest} {dep}\n")


       print(f"-> Archivo '{filename}' guardado correctamente con los vuelos de SOLO SALIDA.")
   except Exception as e:
       print(f"Error al guardar el archivo: {e}")




# NUEVA FUNCIÓN PARA GUARDAR LA LISTA FUSIONADA
def SaveMergedFlights(aircrafts, filename):
   if not aircrafts or aircrafts == -1:
       print("Error: La lista de vuelos fusionados está vacía o es inválida.")
       return -1


   try:
       with open(filename, 'w') as f:
           # Escribimos la cabecera con un solo espacio de separación
           f.write("ID AIRLINE ORIGIN ARRIVAL DESTINATION DEPARTURE\n")


           for a in aircrafts:
               # Verificamos cada dato. Si está vacío (""), ponemos un guion "-"
               aid = a.id if a.id != "" else "-"
               airline = a.company if a.company != "" else "-"
               origin = a.origin if a.origin != "" else "-"
               arrival = a.time_of_landing if a.time_of_landing != "" else "-"
               dest = a.destination if a.destination != "" else "-"
               dep = a.departure_time if a.departure_time != "" else "-"


               # Escribimos la línea separando cada variable con exactamente un espacio
               f.write(f"{aid} {airline} {origin} {arrival} {dest} {dep}\n")


       print(f"Archivo '{filename}' guardado correctamente con los movimientos fusionados.")
   except Exception as e:
       print(f"Error al intentar guardar el archivo: {e}")
