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
from LEBL import *
from aircraft import Aircraft
avion_test = Aircraft("WOW123", "WOW", "LEMD", "08:00", "LEMD", "10:00")
resultado_asignacion = AssignGate(aeropuerto, avion_test)
print('\n', "Resultado de asignar puerta (0 es éxito): ", resultado_asignacion)
lista_actualizada = GateOccupancy(aeropuerto)
print("Estado de las puertas tras la asignación: ")
print(lista_actualizada)




from aircraft import Aircraft




# Test AssignNightGates
aeropuerto = LoadAirportStructure("Terminals.txt")




res_vacio = AssignNightGates(aeropuerto, [])
print(f"Lista vacía: {res_vacio}   (esperado: -1)")




nocturno1 = Aircraft("NOCH01", "VLG", "", "", "LEMD", "07:00")
nocturno2 = Aircraft("NOCH02", "VLG", "", "", "LFPG", "09:00")
no_nocturno = Aircraft("NORM01", "VLG", "LEMD", "06:00", "LEMD", "08:00")




res = AssignNightGates(aeropuerto, [nocturno1, nocturno2, no_nocturno])
print(f"Resultado: {res}   (esperado: 0)")
ocupados = [p for p in GateOccupancy(aeropuerto) if p[1] == True]
print(f"Puertas ocupadas: {len(ocupados)}   (esperado: 2)")
ids = [p[2] for p in ocupados]
print(f"NOCH01 asignado: {'NOCH01' in ids}   (esperado: True)")
print(f"NOCH02 asignado: {'NOCH02' in ids}   (esperado: True)")
print(f"NORM01 ignorado: {'NORM01' not in ids}   (esperado: True)")




# Test FreeGate
res_liberar = FreeGate(aeropuerto, "NOCH01")
print(f"\nLiberar NOCH01: {res_liberar}   (esperado: 0)")
ocupados_tras_free = [p for p in GateOccupancy(aeropuerto) if p[1] == True]
print(f"Puertas ocupadas: {len(ocupados_tras_free)}   (esperado: 1)")
ids_tras_free = [p[2] for p in ocupados_tras_free]
print(f"NOCH01 liberado: {'NOCH01' not in ids_tras_free}   (esperado: True)")
print(f"NOCH02 sigue: {'NOCH02' in ids_tras_free}   (esperado: True)")
res_inexistente = FreeGate(aeropuerto, "NOEXISTE")
print(f"ID inexistente: {res_inexistente}   (esperado: -1)")




# Test AssignGatesAtTime
aeropuerto = LoadAirportStructure("Terminals.txt")




av1 = Aircraft("TEST001", "VLG", "LEMD", "08:00", "LEMD", "10:00")
av2 = Aircraft("TEST002", "VLG", "LFPG", "08:00", "LFPG", "11:00")
av3 = Aircraft("TEST003", "VLG", "LSZH", "10:00", "LSZH", "13:00")
lista_aviones = [av1, av2, av3]




no_asig_8 = AssignGatesAtTime(aeropuerto, lista_aviones, "08:00")
print(f"\nPeriodo 08:00 → sin puerta: {no_asig_8}   (esperado: 0)")
ocupados_8 = [p for p in GateOccupancy(aeropuerto) if p[1] == True]
print(f"Puertas ocupadas: {len(ocupados_8)}   (esperado: 2)")




no_asig_10 = AssignGatesAtTime(aeropuerto, lista_aviones, "10:00")
print(f"Periodo 10:00 → sin puerta: {no_asig_10}   (esperado: 0)")
ocupados_10 = [p for p in GateOccupancy(aeropuerto) if p[1] == True]
print(f"Puertas ocupadas: {len(ocupados_10)}   (esperado: 2)")
ids_ocupados = [p[2] for p in ocupados_10]
print(f"TEST001 liberado: {'TEST001' not in ids_ocupados}   (esperado: True)")
print(f"TEST003 asignado: {'TEST003' in ids_ocupados}   (esperado: True)")




# Test PlotDayOccupancy
aeropuerto_dia = LoadAirportStructure("Terminals.txt")




aviones_dia = [
  Aircraft("DIA001", "VLG", "LEMD", "06:00", "LEMD", "08:00"),
  Aircraft("DIA002", "VLG", "LFPG", "06:00", "LFPG", "09:00"),
  Aircraft("DIA003", "VLG", "LSZH", "07:00", "LSZH", "10:00"),
  Aircraft("DIA004", "VLG", "EDDF", "09:00", "EDDF", "12:00"),
  Aircraft("DIA005", "VLG", "LIRF", "09:00", "LIRF", "11:00"),
  Aircraft("DIA006", "VLG", "EDDM", "17:00", "EDDM", "20:00"),
  Aircraft("NOCHE1", "VLG", "",     "",      "LEMD", "07:00"),
]




nocturnos = [a for a in aviones_dia if a.origin == "" and a.time_of_landing == ""]
AssignNightGates(aeropuerto_dia, nocturnos)
PlotDayOccupancy(aeropuerto_dia, aviones_dia)
