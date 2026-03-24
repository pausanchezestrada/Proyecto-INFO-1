from airport import *

airport = Airport("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport(airport)

lista_aero = LoadAirports("Airports.txt")

AddAirport(lista_aero, airport)

lista_aero = RemoveAirport(lista_aero, "LEBL")

SaveSchengenAirports(lista_aero, "SchengenAirports.txt")

PlotAirports(lista_aero)

MapAirports(lista_aero)