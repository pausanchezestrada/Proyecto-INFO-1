from aircraft import *
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
 # función LoadDepartures
 departures = LoadDepartures("Departures.txt")
 print(f"Departures cargados: {len(departures)}")
 print(
     f"Primer departure: id={departures[0].id} destino={departures[0].destination} hora={departures[0].departure_time}")
 # función MergeMovements
 merged = MergeMovements(arrivals, departures)
 print(f"\nMerged total: {len(merged)}")
 completos = [a for a in merged if a.origin != "" and a.destination != ""]
 solo_llegada = [a for a in merged if a.origin != "" and a.destination == ""]
 solo_salida = [a for a in merged if a.origin == "" and a.departure_time != ""]
 print(f"Con llegada y salida: {len(completos)}")
 print(f"Solo llegada: {len(solo_llegada)}")
 print(f"Solo salida (nocturnos): {len(solo_salida)}")
 # función NightAircraft
 nocturnos = NightAircraft(merged)
 print(f"\nAviones nocturnos: {len(nocturnos)}")
 for a in nocturnos:
     print(f"  id={a.id} destino={a.destination} hora_salida={a.departure_time}")
