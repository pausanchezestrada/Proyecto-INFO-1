class Airport: #definimos la clase airport con sus características
  def __init__(self, ICAOcode, latitude, longitude):
      self.ICAOcode = ICAOcode
      self.latitude = latitude
      self.longitude = longitude
      self.schengen = False

def IsSchengenAirport(code): #funición para hacer la lista para clasificar códigos ICAO en schengen o no
  lista = ['LO', 'EB', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP','LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
  return code[:2] in lista

def SetSchengen(airport): #funición para la clasificación
  airport.schengen = IsSchengenAirport(airport.ICAOcode)

def PrintAirport(airport): #función para mostrar resultados schengen
  print(airport.schengen)

def LoadAirports(filename): #función para cargar la lista de aeropuertos
    if len(filename) == 0:
        return -1
    f = open(filename, "r")
    f.readline()
    linea = f.readline()
    lista_aero = []
    while linea != "":
        elementos = linea.split(" ") #separar elementos linea a linea en nombre y coordenadas.
        nombre = elementos[0]
        #LATITUD en decimales
        latitude = elementos[1]
        letra = latitude[0]
        if letra == "W" or letra == "S":
            direccion = -1
        else:
            direccion = 1
        grados = float(latitude[1:3])
        min = float(latitude[3:5])
        seg = float(latitude[5:7])
        latitud = direccion * (grados + min / 60 + seg / 3600)
        #LONGITUD en decimales
        longitude = elementos[2]
        letra2 = longitude[0]
        if letra2 == "W" or letra2 == "S":
            direccion2 = -1
        else:
            direccion2 = 1
        grados2 = float(longitude[1:4])
        min2 = float(longitude[4:6])
        seg2 = float(longitude[6:8])
        longitud = direccion2 * (grados2 + min2 / 60 + seg2 / 3600)
        nuevo_aeropuerto = Airport(nombre, latitud, longitud)
        lista_aero.append(nuevo_aeropuerto)
        linea = f.readline()
    f.close()
    return lista_aero

def SaveSchengenAirports(airports, filename): #función para cargar SOLAMENTE los schengen
    if len(airports) == 0:
        return -1
    g = open(filename, "w")
    g.write("CODE LAT LON\n")
    for a in airports:
        SetSchengen(a)
        if a.schengen:
            # LATITUD en el formato especificado en el ejemplo (con letras)
            lat = a.latitude
            if lat < 0:
                direccion = "S"
                lat = -lat
            else:
                direccion = "N"
            grados = int(lat)
            minfloat = (lat - grados) * 60
            min = int(minfloat)
            seg = int(round((minfloat - min) * 60))
            if seg == 60:
                seg = 0
                min += 1
            if min == 60:
                min = 0
                grados += 1
            if grados < 10:
                strgrados = "0" + str(grados)
            else:
                strgrados = str(grados)
            if min < 10:
                strmin = "0" + str(min)
            else:
                strmin = str(min)
            if seg < 10:
                strseg = "0" + str(seg)
            else:
                strseg = str(seg)
            strlatitud = str(direccion) + strgrados + strmin + strseg
            lon = a.longitude

            #LONGITUD en el formato especificado en el ejemplo (con letras)
            if lon < 0:
                direccion2 = "W"
                lon = -lon
            else:
                direccion2 = "E"
            grados2 = int(lon)
            minfloat2 = (lon - grados2) * 60
            min2 = int(minfloat2)
            seg2 = int(round((minfloat2 - min2) * 60))
            if seg2 == 60:
                seg2 = 0
                min2 += 1
            if min2 == 60:
                min2 = 0
                grados2 += 1
            if grados2 < 10:
                strgrados2 = "00" + str(grados2)
            elif grados2 < 100:
                strgrados2 = "0" + str(grados2)
            else:
                strgrados2 = str(grados2)
            if min2 < 10:
                strmin2 = "0" + str(min2)
            else:
                strmin2 = str(min2)
            if seg2 < 10:
                strseg2 = "0" + str(seg2)
            else:
                strseg2 = str(seg2)
            lon_str = str(direccion2) + strgrados2 + strmin2 + strseg2
            g.write(str(a.ICAOcode) + " " + strlatitud + " " + lon_str + "\n")
    g.close()
    return 0

def AddAirport(airports, airport): #Añadir aeropuertos a la lista anterior
    # Comparar ICAO con el de la lista de antes
    encontrado = False
    for a in airports:
        if a.ICAOcode == airport.ICAOcode:
            encontrado = True
            break
    if not encontrado: # si no está en esta lista, se añade.
        airports.append(airport)

def RemoveAirport(airports, code): #función para quitar aeropuertos
    posicion = -1
    for i in range(len(airports)):
        if airports[i].ICAOcode == code: # si no está, no lo puede quitar
            posicion = i
            break
    if posicion == -1:
        return -1
    nueva_lista = []
    for i in range(len(airports)):
        if i != posicion:
            nueva_lista.append(airports[i]) # el aeropuerto que queremos quitar se elimina al mover toda la lista
    return nueva_lista

import matplotlib.pyplot as pyplot
def PlotAirports(airports): #función para crear un gráfico APILADO de los schengen y los no schengen
    contador_schengen=0
    contador_NOschengen=0
    i=0
    while i<len(airports):
        a = airports[i]
        SetSchengen(a)
        if a.schengen:
            contador_schengen = contador_schengen+1
        else:
            contador_NOschengen = contador_NOschengen+1
        i=i+1
    pyplot.bar(["Airports"], [contador_schengen], label="Schengen", color="blue") #Eje X
    pyplot.bar(["Airports"], [contador_NOschengen], bottom=[contador_schengen], label="No Schengen", color="red") #Eje Y
    pyplot.title("Schengen airports")
    pyplot.ylabel("Count")
    pyplot.legend()
    pyplot.show()

def MapAirports(airports): #Función para crear archivo kml que pueda leer Google Earth.
    p = open("Airports.kml", "w") #para google earth hay que abrir un archivo kml
    p.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    p.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    p.write('<Document>\n') #empieza el documento kml (para que lo lea goole earth)
    j = 0
    while j < len(airports):
        a = airports[j]
        SetSchengen(a)
        if a.schengen: #comprobar si el aeropuerto es Schengen
            color = "ff0000ff"  # Rojo
        else:
            color = "ff00ff00"  # Verde
        p.write("<Placemark>\n") #con esto creas el marcador
        p.write("<name>" + str(a.ICAOcode) + "</name>\n")
        p.write("<Style>\n")
        p.write("<IconStyle>\n")
        p.write("<color>" + str(color) + "</color>\n")
        p.write("</IconStyle>\n") #color del marcador
        p.write("</Style>\n")
        # para marcar longitud y latitud
        p.write("<Point>\n") #punto geográfico
        coordenadas = str(a.longitude) + "," + str(a.latitude) + ",0"
        p.write("<coordinates>" + coordenadas + "</coordinates>\n")
        p.write("</Point>\n")
        p.write("</Placemark>\n")
        j=j+1
    p.write("</Document>\n") #fin del documento
    p.write("</kml>\n") #fin del archivo kml
    p.close()