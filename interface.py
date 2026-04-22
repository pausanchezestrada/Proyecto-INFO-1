from tkinter import *
from airport import *
from aircraft import *

aeropuerto_creado = []
lista_principal = []
lista_aircraft = []

def AClick():
  nuevo_aero = Airport("LEBL", 41.297445, 2.0832941)
  SetSchengen(nuevo_aero)
  if len(aeropuerto_creado) > 0:
      aeropuerto_creado[0] = nuevo_aero
  else:
      aeropuerto_creado.append(nuevo_aero)
  print("Aeropuerto clasificado.")

def BClick():
  if len(aeropuerto_creado) > 0:
      PrintAirport(aeropuerto_creado[0])

def CClick():
  cargados = LoadAirports("Airports.txt")
  #vaciado manual
  while len(lista_principal) > 0:
      #Movemos cada elemento una posición a la izquierda para aplastar al primero
      for i in range(len(lista_principal) - 1):
          lista_principal[i] = lista_principal[i + 1]
      #Eliminamos el último elemento, que ha quedado duplicado.
      lista_principal[:] = lista_principal[:-1]
  # Llenamos la lista principal con los elementos que queremos
  for a in cargados:
      lista_principal.append(a)
  print("Aeropuertos cargados: " + str(len(lista_principal)))

def DClick():
  if len(aeropuerto_creado) > 0:
      AddAirport(lista_principal, aeropuerto_creado[0])
      print("Aeropuerto añadido. Total ahora: " + str(len(lista_principal)))

def EClick():
  resultado = RemoveAirport(lista_principal, "LEBL")
  if resultado != -1:
      # vaciamos otra vez la lista
      while len(lista_principal) > 0:
          for i in range(len(lista_principal) - 1):
              lista_principal[i] = lista_principal[i + 1]
          lista_principal[:] = lista_principal[:-1]
      # Rellenamos con la nueva lista sin el aeropuerto marcado
      for a in resultado:
          lista_principal.append(a)
      print("Aeropuerto borrado.Total ahora: " + str(len(lista_principal)))

def FClick():
  SaveSchengenAirports(lista_principal, "SchengenAirports.txt")
  print("Archivo SchengenAirports.txt creado.")

def GClick():
  PlotAirports(lista_principal)

def HClick():
  MapAirports(lista_principal)
  print("Archivo Airports.kml creado.")

def IClick():
   aviones = LoadArrivals("Arrivals.txt")
   # vaciado manual
   while len(lista_aircraft) > 0:
       # Movemos cada elemento una posición a la izquierda para aplastar al primero
       for i in range(len(lista_aircraft) - 1):
           lista_aircraft[i] = lista_aircraft[i + 1]
       # Eliminamos el último elemento, que ha quedado duplicado.
       lista_aircraft[:] = lista_aircraft[:-1]
   # Llenamos la lista aircraft con los elementos que queremos
   for a in aviones:
       lista_aircraft.append(a)
   print("Aviones cargados: " + str(len(lista_aircraft)))

def JClick():
   PlotArrivals(lista_aircraft)

def KClick():
   SaveFlights(lista_aircraft,"Arrivals.txt")

def LClick():
   PlotAirlines(lista_aircraft)

def MClick():
   PlotFlightsType(lista_aircraft)

def NClick():
   if len(lista_aircraft)>0:
       MapFlights(lista_aircraft)
       print("Se ha creado el archivo Aircraft.kml")
   else:
       print("No hay ningún vuelo")

def OClick():
   if len(lista_aircraft)>0:
       long_distance_flights=LongDistanceArrivals(lista_aircraft)
       print("vuelos de larga distancia:", len(long_distance_flights))
   else:
       print("No hay vuelos de larga distancia")

window = Tk()
window.geometry("800x800")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)

tituloLabel = Label(window, text="Airports", font=("Courier", 20, "italic"))
tituloLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función SetSchengen
AButton = Button(window, text="SetSchengen", bg='orange', fg="black", command=AClick)
AButton.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función PrintAirport
BButton = Button(window, text="PrintAirport", bg='orange', fg="black", command=BClick)
BButton.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función LoadAirport
CButton = Button(window, text="LoadAirport", bg='orange', fg="black", command=CClick)
CButton.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función AddAirport
DButton = Button(window, text="AddAirport", bg='orange', fg="black", command=DClick)
DButton.grid(row=1, column=3, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función RemoveAirport
EButton = Button(window, text="RemoveAirport", bg='orange', fg="black", command=EClick)
EButton.grid(row=2, column=0, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función SaveSchengenAirports
FButton = Button(window, text="SaveSchengenAirports", bg='orange', fg="black", command=FClick)
FButton.grid(row=2, column=1, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función PlotAirport
GButton = Button(window, text="PlotAirport", bg='orange', fg="black", command=GClick)
GButton.grid(row=2, column=2, padx=5, pady=5, sticky=N + S + E + W)
#botón de la función MapAirport
HButton = Button(window, text="MapAirport", bg='orange', fg="black", command=HClick)
HButton.grid(row=2, column=3, padx=5, pady=5, sticky=N + S + E + W)
#Botón de la función LoadAirports
IButton = Button(window, text="LoadAircrafts", bg='orange', fg="black", command=IClick)
IButton.grid(row=3, column=0, padx=5, pady=5, sticky=N + S + E + W)
#Botón de la función PlotAircrafts
JButton = Button(window, text="PlotAircrafts", bg='orange', fg="black", command=JClick)
JButton.grid(row=3, column=1, padx=5, pady=5, sticky=N + S + E + W)
#Botón de la función SaveFlights
KButton = Button(window, text="SaveFlights", bg='orange', fg="black", command=KClick)
KButton.grid(row=3, column=2, padx=5, pady=5, sticky=N + S + E + W)
#Botón de la función Plot Airlines
LButton = Button(window, text="PlotAirlines", bg='orange', fg="black", command=LClick)
LButton.grid(row=3, column=3, padx=5, pady=5, sticky=N + S + E + W)
#Botón de la función FlightTypes
MButton = Button(window, text="FlightTypes", bg='orange', fg="black", command=MClick)
MButton.grid(row=4, column=0, padx=5, pady=5, sticky=N + S + E + W)
NButton = Button(window, text="MapFlights", bg='orange', fg="black", command=NClick)
NButton.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)
OButton = Button(window, text="LongDistanceFlights", bg='orange', fg="black", command=OClick)
OButton.grid(row=4, column=2, padx=5, pady=5, sticky=N + S + E + W)

window.mainloop()
