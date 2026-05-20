from LEBL import*
# Test función 1
# Crea puertas dentro de una zona de embarque - todas empiezan libres y sin avión
area_A = BoardingArea("Zona A", "Schengen", [])
area_B = BoardingArea("Zona B", "Schengen", [])
area_C = BoardingArea("Zona C", "Schengen", [])
area_D = BoardingArea("Zona D", "non-Schengen", [])
area_E = BoardingArea("Zona E", "non-Schengen", [])
area_M = BoardingArea("Zona M", "Schengen", [])
area_R = BoardingArea("Zona R", "Schengen", [])
area_S = BoardingArea("Zona S", "Schengen", [])
area_U = BoardingArea("Zona U", "Schengen", [])
area_W = BoardingArea("Zona W", "non-Schengen", [])
area_Y = BoardingArea("Zona Y", "non-Schengen", [])

t1 = Terminal("T1", [area_A, area_B, area_C, area_D, area_E], [])
t2 = Terminal("T2", [area_M, area_R, area_S, area_U, area_W, area_Y], [])


# Creamos el aeropuerto pasando su código y la lista con las terminales
aeropuerto = BarcelonaAP("LEBL", [t1, t2])
print("Creando las puertas válidas.\n")
resultado_A = SetGates(area_A, 1, 11, "ABA")
if resultado_A == -1:
   print("Error al generar las puertas de la Zona A.")
else:
   print(f"Puertas generadas con éxito en la {area_A.name}:")
   for puerta in area_A.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupada: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_B = SetGates(area_B, 1, 57, "ABB")
if resultado_B == -1:
   print("Error al generar las puertas de la Zona B.")
else:
   print(f"\nPuertas generadas con éxito en la {area_B.name}:")
   for puerta in area_B.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_C = SetGates(area_C, 1, 11, "ABC")
if resultado_C == -1:
   print("Error al generar las puertas de la Zona C.")
else:
   print(f"\nPuertas generadas con éxito en la {area_C.name}:")
   for puerta in area_C.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_D = SetGates(area_D, 1, 11, "ABD")
if resultado_D == -1:
   print("Error al generar las puertas de la Zona D.")
else:
   print(f"\nPuertas generadas con éxito en la {area_D.name}:")
   for puerta in area_D.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_E = SetGates(area_E, 1, 11, "ABE")
if resultado_E == -1:
   print("Error al generar las puertas de la Zona E.")
else:
   print(f"\nPuertas generadas con éxito en la {area_E.name}:")
   for puerta in area_E.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_M = SetGates(area_M, 1, 8, "ABM")
if resultado_M == -1:
   print("Error al generar las puertas de la Zona M.")
else:
   print(f"\nPuertas generadas con éxito en la {area_M.name}:")
   for puerta in area_M.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_R = SetGates(area_R, 9, 19, "ABR")
if resultado_R == -1:
   print("Error al generar las puertas de la Zona R.")
else:
   print(f"\nPuertas generadas con éxito en la {area_R.name}:")
   for puerta in area_R.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_S = SetGates(area_S, 20, 30, "ABS")
if resultado_S == -1:
   print("Error al generar las puertas de la Zona S.")
else:
   print(f"Puertas generadas con éxito en la {area_S.name}:")
   for puerta in area_S.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_U = SetGates(area_U, 30, 39, "ABU")
if resultado_U == -1:
   print("Error al generar las puertas de la Zona S.")
else:
   print(f"\nPuertas generadas con éxito en la {area_U.name}:")
   for puerta in area_U.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_W = SetGates(area_W, 40, 49, "ABW")
if resultado_W == -1:
   print("Error al generar las puertas de la Zona W.")
else:
   print(f"\nPuertas generadas con éxito en la {area_W.name}:")
   for puerta in area_W.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")
resultado_Y = SetGates(area_Y, 50, 59, "ABY")
if resultado_Y == -1:
   print("Error al generar las puertas de la Zona Y.")
else:
   print(f"\nPuertas generadas con éxito en la {area_Y.name}:")
   for puerta in area_Y.list:
       print(f" -> Nombre: {puerta.Gate_name} | Ocupancy: {puerta.Gate_occupancy} | Avión: {puerta.Gate_aircraft_id}")

# Test función 2
LoadAirlines(t1, "T1")
print("Códigos ICAO de la T1:", t1.Icao)
LoadAirlines(t2, "T2")
print("Códigos ICAO de la T2:", t2.Icao)

# Test función 3
print("\n Cargando estructura desde el archivo")
aeropuerto = LoadAirportStructure("Terminals.txt")
print("Código del aeropuerto cargado:", aeropuerto.code)
for t in aeropuerto.terminal:
   print(t.name)
for area in t.BoardingArea:
   print(area.name)
   for puerta in area.list:
       print("  Gate: ", puerta.Gate_name)

# Test función 4
lista_de_puertas = GateOccupancy(aeropuerto)
print('\n', "Todas las puertas y su estado: ")
print(lista_de_puertas)

# Test función 5
first_airline = IsAirlineInTerminal(t1, "ADR")
second_airline = IsAirlineInTerminal(t2, "EIN")
print('\n', "Esa aerolinea esta en la T1?: ", first_airline)
print("Esa aerolinea esta en la T2?: ", second_airline)

# Test función 6
search_terminal = SearchTerminal(aeropuerto, "WOW")
print('\n', "La terminal dónde se encuentra la aerolinea es en la: ", search_terminal)

# Test función 7
class Aircraft:
   def __init__(self, id_av, aerolinea, tipo):
       self.aircraft_id = id_av
       self.airline_icao = aerolinea
       self.flight_type = tipo
avion_test = Aircraft("WOW123", "WOW", "Schengen")
resultado_asignacion = AssignGate(aeropuerto, avion_test)
print('\n', "Resultado de asignar puerta (0 es éxito): ", resultado_asignacion)
lista_actualizada = GateOccupancy(aeropuerto)
print("Estado de las puertas tras la asignación: ")
print(lista_actualizada)
