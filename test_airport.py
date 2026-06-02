from airport import *
from aircraft import *


airport = Airport("LEBL", 41.645468, 2.853789)
SetSchengen(airport)
PrintAirport(airport)


lista_aero = LoadAirports("Airports.txt")


AddAirport(lista_aero, airport)


lista_aero = RemoveAirport(lista_aero, "EBBR")


SaveSchengenAirports(lista_aero, "SchengenAirports.txt")


PlotAirports(lista_aero)


MapAirports(lista_aero)


lista_aircraft = LoadArrivals("Arrivals.txt")
print(lista_aircraft)
PlotArrivals(lista_aircraft)
SaveFlights(lista_aircraft,"Flights.txt")
print(lista_aircraft)
PlotAirlines(lista_aircraft)
PlotFlightsType(lista_aircraft)
MapFlights(lista_aircraft)
print("Se ha generado el mapa de vuelos")
#función LongDistanceArrivals
long_distance_flights=LongDistanceArrivals(lista_aircraft)
print("Número de vuelos de larga distancia:", len(long_distance_flights))

