#FUNCIÓN 1
class Aircraft:
  def __init__(self, aircraft_id, company, origin, landing_time):
      self.id = aircraft_id
      self.company = company
      self.origin = origin
      self.time_of_landing = landing_time
def LoadArrivals(filename):
  arrivals = []
  try:
      file = open(filename, 'r')
  except FileNotFoundError:
      return arrivals #Devuelve una lista vacia si el archivo no existe
  lines = file.readlines()
  file.close()
  if len(lines) <= 1:
      return arrivals #Si solo tiene cabecera o está vacío,devuelve una lista vacía
  i = 1 #Indice para saltar la cabecera
  line = lines[i]
  while i < len(lines) and line != '':
      parts = line.split()
      if len(parts) == 4: #se verifica que tenga los 4 campos esperados
          aircraft_id = parts[0]
          origin = parts[1]
          time_str = parts[2]
          company = parts[3]
          if len(origin) == 4 and len(company) == 3 and len(time_str) == 5:  #validación de los digitos del documento dado
              if time_str[2] == ':': #verificación de que el tercer carácter sea dos puntos
                  digitos_validos = True
                  posicion = 0 #indice para recorrer la cadena de tiempo
                  while posicion < 5 and digitos_validos:
                      if posicion != 2: #la posición 2 corresponde al carácter ':'
                          caracter = time_str[posicion] #carácter actual a examinar
                          if not ('0' <= caracter <= '9'): #valida si no es un dígito
                              digitos_validos = False #marca como inválido
                      posicion = posicion + 1
                  if digitos_validos:
                      hour_str = time_str[0] + time_str[1] #Crea una cadena con los dos dígitos de la hora
                      minute_str = time_str[3] + time_str[4] #Crea una cadena con los dos dígitos de los minut
                      hour = int(hour_str)
                      minute = int(minute_str)
                      if 0 <= hour <= 23 and 0 <= minute <= 59: #valida que el horario pueda ser real
                          nuevo_vuelo = Aircraft(aircraft_id, company, origin, time_str)
                          arrivals.append(nuevo_vuelo)
      i = i + 1
      if i < len(lines):
          line = lines[i]
  return arrivals

#FUNCIÓN 2
def PlotArrivals(aircrafts):
  #Verificar si la lista está vacía (usando el nombre correcto: aircrafts)
  if not aircrafts:
      print("Error: la lista de aircraft está vacía")
      return
  #Inicializar frecuencias (24 horas)
  frecuencias = [0] * 24
  #Recorrer la lista de objetos Aircraft
  i = 0
  for i in aircrafts:
      try:
          # Extraer la hora del atributo time_of_landing (formato "HH:MM")
          # split(":") separa "05:47" en ["05", "47"], y cogemos el [0]
          hora = int(i.time_of_landing.split(":")[0])
          if 0 <= hora <= 23:
              frecuencias[hora] += 1
      except (ValueError, AttributeError, IndexError):
          #Si el dato está mal, saltamos ese avión y seguimos con el resto
          continue
  #Configuración del gráfico
  horas = list(range(24))
  plt.figure(figsize=(10, 5))
  plt.bar(horas, frecuencias, color='royalblue', edgecolor='black')
  plt.xlabel("Hora del día")
  plt.ylabel("Número de llegadas")
  plt.title("Frecuencia de llegadas por hora")
  plt.xticks(horas)
  plt.grid(axis='y', linestyle='--', alpha=0.7)
  plt.show()

#FUNCIÓN 3
def SaveFlights(aircrafts, filename):
#Si la lista está vacía, no se crea el archivo y devolvemos un código de error
   if not aircrafts:
      print("Error: La lista de aeronaves está vacía. No se ha creado ningún archivo.")
      return -1
   try:
       with open(filename, 'w') as f:
   #Escribimos la cabecera (opcional, pero recomendada para el formato de entrada)
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

#FUNCIÓN 4
import matplotlib.pyplot as plt
def PlotAirlines(aircrafts):
  if len(aircrafts) == 0: #Verifica si la lista está vacia
      print("La lista de vuelos esta vacía y no se puede mostrar el gráfico.")
      return
  companies = [] #lista para códigos de aerolíneas únicas
  frequencies = [] #lista para contar la frecuencia de los vuelos en una aerolinea
  i = 0
  while i < len(aircrafts):
      current_company = aircrafts[i].company
      found = False #sirve para saber si ya existe en companies
      j = 0
      while j < len(companies) and not found: #busca la compañía
          if companies[j] == current_company:
              frequencies[j] = frequencies[j] + 1
              found = True
          j = j + 1
      if not found:
          companies.append(current_company) #si es una aerolínea nueva la añade a la lista
          frequencies.append(1) #inicia su frecuencia en 1
      i = i + 1
  plt.bar(companies, frequencies)
  plt.title("Número de vuelos por aerolinea")
  plt.xlabel("Aerolinea (ICAO)")
  plt.ylabel("Cantidad de vuelos")
  plt.xticks(rotation=90, fontsize=5)
  plt.show() #muestra el gráfico con todas las características dadas justo en las lineas anteriores

# FUNCIÓN 5
def PlotFlightsType(aircrafts):
  if len(aircrafts) == 0: #verifica si la lista está vacía
      print("La lista de vuelos esta vacia y no se puede mostrar el grafico.")
      return
  #lista de prefijos ICAO de países Schengen
  prefijos_schengen = ['LE', 'LF', 'ED', 'EB', 'EH', 'LI', 'LS', 'LO', 'LK', 'LZ', 'LD', 'LG', 'LP', 'LR', 'LU', 'LW', 'LY', 'LA', 'LB', 'LC', 'LJ', 'LM', 'LN', 'LV', 'LX', 'EP', 'ES', 'ET', 'EV', 'EY', 'BI', 'BK', 'EN', 'GC', 'GM', 'DA', 'DT', 'DR', 'DX', 'DI', 'OE', 'OJ', 'OS', 'LT', 'LQ', 'UB', 'UD', 'UG', 'UK', 'UM', 'UT', 'UA', 'UU', 'UW', 'UY', 'UR', 'UL', 'UN', 'UI', 'UH', 'UE', 'UF', 'US', 'UM', 'UT', 'UA', 'UU', 'UW', 'UY', 'UR', 'UL', 'UN', 'UI', 'UH', 'UE', 'UF', 'US']
  contador_schengen = 0
  contador_no_schengen = 0
  i = 0
  while i < len(aircrafts):
      origin = aircrafts[i].origin #Obtiene el código ICAO del aeropuerto de origen
      prefijo = origin[0] + origin[1] #extrae las dos primeras letras (prefijo de país)
      si_schengen = False
      j = 0
      while j < len(prefijos_schengen) and not si_schengen: #busca el prefijo en la lista Schengen
          if prefijos_schengen[j] == prefijo:
              si_schengen = True
          j = j + 1
      if si_schengen: #Incrementa el contador correspondiente a si el vuelo tiene o no origen schengen
          contador_schengen = contador_schengen + 1
      else:
          contador_no_schengen = contador_no_schengen + 1
      i = i + 1
  categoria_unica_ejeX = ['Vuelos'] #Componentes eje X (solo hay una porque es un grafico apilado)
  valor_schengen = [contador_schengen] #Valores de la parte Schengen
  valor_no_schengen = [contador_no_schengen] #valore    s de la parte no Schengen
  plt.bar(categoria_unica_ejeX, valor_schengen, label='Schengen') #Dibuja la barra base (Schengen)
  plt.bar(categoria_unica_ejeX, valor_no_schengen, bottom=valor_schengen, label='No Schengen') #Apila encima la barra no Schengen
  plt.title("Vuelos desde paises Schengen y no Schengen")
  plt.ylabel("Cantidad de vuelos")
  plt.legend()
  plt.show()

 #FUNCIÓN 6
def MapFlights (aircrafts):
  from airport import IsSchengenAirport, LoadAirports
  # el aeropuerto de destino es siempre el Prat:
  latitud_LEBL = 41.2971
  longitud_LEBL = 2.0785
  k=open("Aircrafts.kml","w")
  k.write('<?xml version="1.0" encoding="UTF-8"?>\n')
  k.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
  k.write('<Document>\n')
  lista_aero = LoadAirports("Airports.txt")  # sacamos la función y la lista de aeropuertos de la versión 1
  for flight in aircrafts:
      #necesitamos encontrar las coordenadas del aeropuerto de origen porque en la clase airport solo tenemos el ICAO
      #necesitamos el encontrado para que solo marque los aeropuertos que existen en la lista. si no existe daría error
      encontrado=False
      origen_latitud=0
      origen_longitud=0
      for a in lista_aero:
          if a.ICAOcode==flight.origin:
              origen_latitud=a.latitude
              origen_longitud=a.longitude
              encontrado=True
              break
      if encontrado:
          if IsSchengenAirport(flight.origin):
              color="ff0000ff"
          else:
              color="ff00ff00"
          #el código siguiente es para describir la línea (la estética)
          k.write("<Placemark>")
          k.write(f'<name>Flight {flight.id}</name>\n')  #primero definimos el nombre del vuelo
          k.write('<Style>\n')
          k.write('<LineStyle>\n')            #antes era IconStyle, pero ahora es line porque estamos definiendo una línea
          k.write(f'<color>{color}</color>\n')          #color de la línea
          k.write('<width>2</width>\n')           #al ser una línea también hay que añadirle la anchura
          k.write('</LineStyle>\n')
          k.write('</Style>\n')
          #a partir de aquí definimos las coordenadas
          k.write('<LineString>\n')            #Antes era Point - punto geográfico, ahora es line string
          k.write('<coordinates>\n')   #Ahora vienen las coordenadas
          k.write(f'{origen_longitud},{origen_latitud},0 {longitud_LEBL},{latitud_LEBL},0')
          k.write('\n</coordinates>\n')
          k.write('</LineString>\n')
          k.write('</Placemark>\n')
  #cerramos el archivo kml
  k.write('</Document>\n')
  k.write('</kml>\n')
  k.close()

#FUNCIÓN 7
# Definir vuelos de larga distancia
import math
from airport import LoadAirports
def Haversine3(lat1,lon1,lat2,lon2): #Sirve para calcular la distancia entre dos puntos
  R_tierra=6371 #es el radio de la tierra en km (se necesita en la fórmula)
  #pasamos de grados a radianes
  rad_lat1=math.radians(lat1)
  rad_lat2=math.radians(lat2)
  rad_lon1=math.radians(lon1)
  rad_lon2=math.radians(lon2)
  dphi = math.radians(lat2 - lat1)
  dlambda = math.radians(lon2 - lon1)
  #Aplicamos la fórmula de Harvesine:
  a = math.sin(dphi / 2) ** 2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(dlambda / 2) ** 2
  b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  return R_tierra * b

def LongDistanceArrivals(aircrafts):
  #el aeropuerto de destino es siempre el Prat
  latitud_LEBL = 41.2971
  longitud_LEBL = 2.0785
  #Ahora hay que buscar las coordenadas del aeropuerto de origen igual que hemos hecho en la función de GE
  lista_aero=LoadAirports("Airports.txt")
  long_distance_flights=[]
  for flight in aircrafts:
      # necesitamos encontrar las coordenadas del aeropuerto de origen porque en la clase airport solo tenemos el ICAO
      # necesitamos el encontrado para que solo marque los aeropuertos que existen en la lista. si no existe daría error
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
          distancia=Haversine3(origen_latitud,origen_longitud,latitud_LEBL,longitud_LEBL)
          if distancia>2000:
              long_distance_flights.append(flight)
  return long_distance_flights

#Test de la Versión 2
if __name__ == "__main__":
   #función LoadArrivals
   arrivals=LoadArrivals("Arrivals.txt")
   #función PlotArrivals
   PlotArrivals(arrivals)
   #función SaveFlights
   SaveFlights(arrivals,"Flights.txt")
   #función PlotAirlines
   PlotAirlines(arrivals)
   #función PlotFlightsType
   PlotFlightsType(arrivals)
   #funición MapFlights
   MapFlights(arrivals)
   print("Se ha generado el mapa de vuelos")
   #función LongDistanceArrivals
   long_distance_flights=LongDistanceArrivals(arrivals)
   print("Número de vuelos de larga distancia:", len(long_distance_flights))
