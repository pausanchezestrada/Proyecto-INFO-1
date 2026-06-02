from airport import *
from tkinter import *
import re
import os
from aircraft import *
from LEBL import *
from tkinter import simpledialog
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ANULACIÓN DE plt.show()
plt.show = lambda *args, **kwargs: None

# VARIABLES GLOBALES
aeropuerto_creado = []
lista_principal = []
lista_aircraft = []

# INICIALIZACIÓN DE LA ESTRUCTURA
area = BoardingArea("Zona A", "Schengen", [])
t1 = Terminal("T1", [area], [])
aeropuerto = BarcelonaAP("LEBL", [t1])

# FUNCIÓN FORMATER/EXTRACTOR AVANZADO DE PUERTAS
def extraer_zona_num(nombre):
  match = re.search(r'^(T[12]BA[A-Z])G(\d+)$', nombre)
  if match:
      return match.group(1), int(match.group(2))
  match_viejo = re.search(r'^(.*?)(\d+)$', nombre)
  if match_viejo:
      zona = match_viejo.group(1).rstrip('Gg')
      return zona, int(match_viejo.group(2))
  return nombre, 0

# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA BASE Y CONTENEDORES
window = Tk()
window.title("Gestor del Aeropuerto de Barcelona (LEBL)")
window.state("zoomed")

frame_izquierdo = Frame(window, padx=10, pady=10)
frame_izquierdo.pack(side=LEFT, fill=BOTH, expand=True)

frame_derecho = Frame(window, padx=20, pady=20)
frame_derecho.pack(side=RIGHT, fill=BOTH, expand=True)

# Frames de menús
frame_menu_principal = Frame(frame_izquierdo)
frame_menu_1 = Frame(frame_izquierdo)
frame_menu_2 = Frame(frame_izquierdo)
frame_menu_3 = Frame(frame_izquierdo)
frame_menu_s = Frame(frame_izquierdo)

def mostrar_menu(menu_destino):
  frame_menu_principal.pack_forget()
  frame_menu_1.pack_forget()
  frame_menu_2.pack_forget()
  frame_menu_3.pack_forget()
  frame_menu_s.pack_forget()
  menu_destino.pack(fill=BOTH, expand=True)

# Contenedores del Panel Derecho
lbl_salida = Label(frame_derecho, text="Consola de Ejecución / Gráficos:", font=("Arial", 12, "bold"))
lbl_salida.pack(anchor=W, pady=(0, 10))

frame_texto = Frame(frame_derecho)
frame_grafico = Frame(frame_derecho)
frame_mapa = Frame(frame_derecho)

frame_texto.pack(fill=BOTH, expand=True)
area_resultado = Text(frame_texto, wrap=WORD, background="#1e1e1e", fg="#ffffff", font=("Consolas", 11))
area_resultado.insert(END, "Esperando ejecución de comandos...\n")
area_resultado.config(state="disabled")
area_resultado.pack(fill=BOTH, expand=True)

# FUNCIONES DE CONTROL DE PANTALLA (TEXTO, GRÁFICO, MAPA)
def mostrar_en_pantalla(texto):
  frame_grafico.pack_forget()
  frame_mapa.pack_forget()
  frame_texto.pack(fill=BOTH, expand=True)

  #LIMPIAR CUADROS DE BÚSQUEDA INTERACTIVOS PREVIOS
  for widget in frame_texto.winfo_children():
      if widget != area_resultado:
          widget.destroy()

  area_resultado.config(state="normal")
  area_resultado.delete("1.0", END)
  area_resultado.insert(END, texto + "\n")
  area_resultado.config(state="disabled")

def mostrar_grafico_en_pantalla():
  frame_texto.pack_forget()
  frame_mapa.pack_forget()
  frame_grafico.pack(fill=BOTH, expand=True)

  for widget in frame_grafico.winfo_children():
      widget.destroy()

  try:
      fig = plt.gcf()
      canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
      canvas.draw()
      canvas_widget = canvas.get_tk_widget()
      canvas_widget.pack(fill=BOTH, expand=True)
  except Exception as e:
      print(f"Error al renderizar gráfico: {e}")

def mostrar_kml_en_pantalla(nombre_archivo):
  frame_texto.pack_forget()
  frame_grafico.pack_forget()
  frame_mapa.pack(fill=BOTH, expand=True)

  for widget in frame_mapa.winfo_children():
      widget.destroy()

  try:
      import tkintermapview
  except ImportError:
      frame_mapa.pack_forget()
      frame_texto.pack(fill=BOTH, expand=True)
      mostrar_en_pantalla(f"Archivo '{nombre_archivo}' guardado de forma local.\n\n"
                          f"[AVISO]: Instala tkintermapview en tu terminal para verlo aquí:\npip install tkintermapview")
      return

  map_widget = tkintermapview.TkinterMapView(frame_mapa, corner_radius=0)
  map_widget.pack(fill=BOTH, expand=True)
  map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", max_zoom=22)

  if not os.path.exists(nombre_archivo):
      return
  with open(nombre_archivo, "r", encoding="utf-8") as f:
      contenido = f.read()

  puntos_coordenadas = []

  placemarks = re.findall(r'<Placemark>.*?<name>(.*?)</name>.*?<coordinates>\s*([\d\.-]+),([\d\.-]+)', contenido, re.DOTALL)
  for name, lon, lat in placemarks:
      lat_f, lon_f = float(lat), float(lon)
      map_widget.set_marker(lat_f, lon_f, text=name)
      puntos_coordenadas.append((lat_f, lon_f))

  lineas = re.findall(r'<LineString>.*?<coordinates>(.*?)</coordinates>', contenido, re.DOTALL)
  for lista_coords in lineas:
      coordenadas_linea = []
      for par in re.findall(r'([\d\.-]+),([\d\.-]+)', lista_coords):
          coordenadas_linea.append((float(par[1]), float(par[0])))
      if coordenadas_linea:
          map_widget.set_path(coordenadas_linea)
          puntos_coordenadas.extend(coordenadas_linea)

  if puntos_coordenadas:
      avg_lat = sum(p[0] for p in puntos_coordenadas) / len(puntos_coordenadas)
      avg_lon = sum(p[1] for p in puntos_coordenadas) / len(puntos_coordenadas)
      map_widget.set_position(avg_lat, avg_lon)
      map_widget.set_zoom(4)
  else:
      map_widget.set_position(41.297445, 2.0832941)
      map_widget.set_zoom(12)

#FUNCIONES DE LOS BOTONES (A - O)
def AClick():
  nuevo_aero = Airport("LEBL", 41.297445, 2.0832941)
  SetSchengen(nuevo_aero)
  if len(aeropuerto_creado) > 0: aeropuerto_creado[0] = nuevo_aero
  else: aeropuerto_creado.append(nuevo_aero)
  mostrar_en_pantalla("Aeropuerto LEBL cargado.")

def BClick():
  if len(aeropuerto_creado) > 0:
      PrintAirport(aeropuerto_creado[0])
      mostrar_en_pantalla("Aeropuerto LEBL clasificado.")

def CClick():
  cargados = LoadAirports("Airports.txt")
  lista_principal.clear()
  lista_principal.extend(cargados)
  mostrar_en_pantalla("Aeropuertos cargados: " + str(len(lista_principal)))

def DClick():
  codigo = simpledialog.askstring("Añadir aeropuerto", "Introduce código ICAO:", parent=window)
  if not codigo:
      mostrar_en_pantalla("Operación cancelada.")
      return

  latitud_texto = simpledialog.askstring("Añadir aeropuerto", "Introduce latitud decimal:", parent=window)
  if not latitud_texto:
      mostrar_en_pantalla("Operación cancelada.")
      return

  longitud_texto = simpledialog.askstring("Añadir aeropuerto", "Introduce longitud decimal:", parent=window)
  if not longitud_texto:
      mostrar_en_pantalla("Operación cancelada.")
      return

  codigo = codigo.upper()

  if len(codigo) != 4:
      mostrar_en_pantalla("Error: el código ICAO debe tener 4 letras.")
      return

  try:
      latitud = float(latitud_texto)
      longitud = float(longitud_texto)
  except:
      mostrar_en_pantalla("Error: la latitud y longitud deben ser números.")
      return

  nuevo_aeropuerto = Airport(codigo, latitud, longitud)
  SetSchengen(nuevo_aeropuerto)
  AddAirport(lista_principal, nuevo_aeropuerto)

  mostrar_en_pantalla(
      "Aeropuerto añadido correctamente.\n"
      "ICAO: " + codigo + "\n"
      "Latitud: " + str(latitud) + "\n"
      "Longitud: " + str(longitud) + "\n"
      "Schengen: " + str(nuevo_aeropuerto.schengen) + "\n\n"
      "Total aeropuertos en memoria: " + str(len(lista_principal))
  )

def EClick():
  codigo = simpledialog.askstring(
      "Eliminar aeropuerto",
      "Introduce el código ICAO a eliminar:",
      parent=window
  )

  if not codigo:
      mostrar_en_pantalla("Operación cancelada.")
      return

  codigo = codigo.upper()

  resultado = RemoveAirport(lista_principal, codigo)

  if resultado != -1:
      lista_principal.clear()
      lista_principal.extend(resultado)
      mostrar_en_pantalla(
          "Aeropuerto eliminado correctamente.\n"
          "ICAO: " + codigo + "\n"
          "Total aeropuertos restantes: " + str(len(lista_principal))
      )
  else:
      mostrar_en_pantalla(
          "No se encontró ningún aeropuerto con ICAO: " + codigo
      )

def FClick():
  SaveSchengenAirports(lista_principal, "SchengenAirports.txt")
  mostrar_en_pantalla("Archivo SchengenAirports.txt creado. Servirá para ver los aeropuertos en el mapa")

def GClick():
  plt.figure()
  PlotAirports(lista_principal)
  mostrar_grafico_en_pantalla()

def HClick():
  MapAirports(lista_principal)
  mostrar_kml_en_pantalla("Airports.kml")

def IClick():
  ruta_archivo = filedialog.askopenfilename(title="Selecciona el archivo de llegadas", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
  if not ruta_archivo:
      mostrar_en_pantalla("⚠️ Operación cancelada: No se seleccionó ningún archivo.")
      return
  try:
      aviones = LoadArrivals(ruta_archivo)
      lista_aircraft.clear()
      lista_aircraft.extend(aviones)
      nombre_archivo = os.path.basename(ruta_archivo)
      mostrar_en_pantalla(f"✅ Archivo '{nombre_archivo}' cargado con éxito.\n✈️ Aviones cargados: {len(lista_aircraft)}")
  except Exception as e:
      mostrar_en_pantalla(f"❌ Error al intentar cargar el archivo:\n{e}")

def JClick():
  plt.figure()
  PlotArrivals(lista_aircraft)
  mostrar_grafico_en_pantalla()

def KClick():
  SaveFlights(lista_aircraft, "Flights.txt")
  mostrar_en_pantalla("Vuelos guardados en Flights.txt")
  mostrar_en_pantalla("Esto sirve para luego ver el recorrido de los vuelos en el mapa")
def LClick():
  plt.figure()
  PlotAirlines(lista_aircraft)
  mostrar_grafico_en_pantalla()

def MClick():
  plt.figure()
  PlotFlightsType(lista_aircraft)
  mostrar_grafico_en_pantalla()

def NClick():
  if lista_aircraft:
      MapFlights(lista_aircraft)
      mostrar_kml_en_pantalla("Aircrafts.kml")
  else:
      mostrar_en_pantalla("No hay ningún vuelo en memoria.")

def OClick():
  if lista_aircraft:
      long_distance_flights = LongDistanceArrivals(lista_aircraft)
      mostrar_en_pantalla(f"Vuelos totales que superan los 2000 km en distancia: {len(long_distance_flights)}")
  else:
      mostrar_en_pantalla("No hay vuelos de larga distancia")

# FUNCIONES DE TESTS Y PANELES (MENÚ 3)
def RunTest1():
  texto_salida = "Creando todas las puertas con el formato estructural unificado...\n"
  configuracion_puertas = [(1, 10, "AG"), (1, 57, "BG"), (1, 11, "CG"), (1, 11, "DG"), (1, 11, "EG"), (1, 8, "MG"), (9, 19, "RG"), (20, 30, "SG"), (30, 39, "UG"), (40, 49, "WG"), (50, 59, "YG")]
  puertas_acumuladas = []
  for inicio, fin, prefijo in configuracion_puertas:
      area_temp = BoardingArea(f"Muelle {prefijo.rstrip('Gg')}", "Schengen", [])
      resultado = SetGates(area_temp, inicio, fin, prefijo)
      if resultado == -1: texto_salida += f"Error al generar las puertas del bloque {prefijo}.\n"
      else:
          puertas_generadas = getattr(area_temp, 'list', [])
          puertas_acumuladas.extend(puertas_generadas)
          for puerta in puertas_generadas:
              texto_salida += f" -> Nombre: {getattr(puerta, 'Gate_name', '')} | Ocupada: {getattr(puerta, 'Gate_occupancy', False)}\n"
          texto_salida += "\n"
  area.list = puertas_acumuladas
  texto_salida += f"TOTAL DE PUERTAS GENERADAS EN MEMORIA: {len(area.list)}\n"
  mostrar_en_pantalla(texto_salida)

def RunTest2():
  t1_test = Terminal("T1", [], [])
  t2_test = Terminal("T2", [], [])
  LoadAirlines(t1_test, "T1")
  LoadAirlines(t2_test, "T2")
  mostrar_en_pantalla(f"Códigos ICAO de la T1: {t1_test.Icao}\n\nCódigos ICAO de la T2: {t2_test.Icao}")

def RunTest3():
  aeropuerto_test = LoadAirportStructure("Terminals.txt")
  texto = f"Cargando estructura desde el archivo\nCódigo del aeropuerto cargado: {aeropuerto_test.code}\n"
  for t in aeropuerto_test.terminal:
      texto += f"\n{t.name}:\n"
      for a in t.BoardingArea:
          texto += f"  {a.name} -> {len(a.list)} puertas cargadas.\n"
  mostrar_en_pantalla(texto)

def RunTest5():
  # 1. Preparamos el panel derecho asegurando que se vea el texto
  frame_grafico.pack_forget()
  frame_mapa.pack_forget()
  frame_texto.pack(fill=BOTH, expand=True)

  # 2. Limpiamos entradas viejas que hayan quedado en el contenedor
  for widget in frame_texto.winfo_children():
      if widget != area_resultado:
          widget.destroy()

  # 3. Quitamos un momento la consola negra para meter el buscador arriba
  area_resultado.pack_forget()

  # 4. Creamos la barra de entrada blanca/gris en la parte superior derecha
  frame_input = Frame(frame_texto, pady=10)
  frame_input.pack(fill=X)

  Label(frame_input, text="Código de aerolínea (ej. ADR):", font=("Arial", 11, "bold")).pack(side=LEFT, padx=5)
  entry_airline = Entry(frame_input, font=("Arial", 11), width=15)
  entry_airline.pack(side=LEFT, padx=5)
  entry_airline.focus_set()  # Pone el cursor de escritura automáticamente aquí

  # Función interna que se ejecutará al darle al botón verde
  def procesar_busqueda_t5():
      codigo = entry_airline.get().strip().upper()
      if not codigo:
          mostrar_en_pantalla("⚠️ Operación cancelada: No escribiste ninguna aerolínea.")
          return

      # Cargamos los datos de prueba
      t1_test = Terminal("T1", [], [])
      t2_test = Terminal("T2", [], [])
      LoadAirlines(t1_test, "T1")
      LoadAirlines(t2_test, "T2")

      first_airline = IsAirlineInTerminal(t1_test, codigo)
      second_airline = IsAirlineInTerminal(t2_test, codigo)

      # Volvemos a dejar la consola limpia y mostramos el resultado
      mostrar_en_pantalla(
          f"🔍 RESULTADO DE VERIFICACIÓN ({codigo}):\n"
          f"----------------------------------------\n"
          f"¿Está en la Terminal 1 (T1)?: {'SÍ ✅' if first_airline else 'NO ❌'}\n"
          f"¿Está en la Terminal 2 (T2)?: {'SÍ ✅' if second_airline else 'NO ❌'}"
      )

  btn_buscar = Button(frame_input, text="Verificar", bg="#4caf50", fg="white", font=("Arial", 10, "bold"),
                      command=procesar_busqueda_t5)
  btn_buscar.pack(side=LEFT, padx=10)

  # 5. Volvemos a colocar la consola negra abajo de todo
  area_resultado.pack(fill=BOTH, expand=True)

  # Mensaje provisional en la consola
  area_resultado.config(state="normal")
  area_resultado.delete("1.0", END)
  area_resultado.insert(END, "⌨️ Escribe el código de la aerolínea en el cuadro superior y pulsa 'Verificar'...\n")
  area_resultado.config(state="disabled")

def RunTest6():
  # 1. Preparamos el panel derecho
  frame_grafico.pack_forget()
  frame_mapa.pack_forget()
  frame_texto.pack(fill=BOTH, expand=True)

  # 2. Limpiamos entradas viejas
  for widget in frame_texto.winfo_children():
      if widget != area_resultado:
          widget.destroy()

  # 3. Quitamos la consola un momento
  area_resultado.pack_forget()

  # 4. Creamos la barra de entrada en la parte superior derecha
  frame_input = Frame(frame_texto, pady=10)
  frame_input.pack(fill=X)

  Label(frame_input, text="Buscar Terminal para (ej. WOW):", font=("Arial", 11, "bold")).pack(side=LEFT, padx=5)
  entry_airline = Entry(frame_input, font=("Arial", 11), width=15)
  entry_airline.pack(side=LEFT, padx=5)
  entry_airline.focus_set()

  # Función interna que se ejecutará al darle al botón azul
  def procesar_busqueda_t6():
      codigo = entry_airline.get().strip().upper()
      if not codigo:
          mostrar_en_pantalla("⚠️ Operación cancelada: No escribiste ninguna aerolínea.")
          return

      aeropuerto_test = LoadAirportStructure("Terminals.txt")
      search_terminal = SearchTerminal(aeropuerto_test, codigo)

      # Si tu función devuelve None o un texto vacío cuando no la encuentra
      if search_terminal:
          resultado_texto = f"La terminal donde se encuentra la aerolínea {codigo} es: {search_terminal} 🏢"
      else:
          resultado_texto = f"La aerolínea '{codigo}' no se encuentra registrada en ninguna terminal. ❌"

      mostrar_en_pantalla(
          f"🔍 LOCALIZACIÓN DE TERMINAL:\n"
          f"----------------------------------------\n"
          f"{resultado_texto}"
      )

  btn_buscar = Button(frame_input, text="Buscar Ubicación", bg="#2196f3", fg="white", font=("Arial", 10, "bold"),
                      command=procesar_busqueda_t6)
  btn_buscar.pack(side=LEFT, padx=10)

  # 5. Re-empaquetamos la consola abajo
  area_resultado.pack(fill=BOTH, expand=True)

  # Mensaje provisional en la consola
  area_resultado.config(state="normal")
  area_resultado.delete("1.0", END)
  area_resultado.insert(END,
                        "⌨️ Escribe el código de la aerolínea en el cuadro superior y pulsa 'Buscar Ubicación'...\n")
  area_resultado.config(state="disabled")

# --------------------------------------------------------

def RunTestNightGates():
  global aeropuerto  # <-- CORRECCIÓN: Usamos la variable global para que los cambios persistan
  aeropuerto = LoadAirportStructure("Terminals.txt")
  texto_salida = "\n--- TEST: AssignNightGates leyendo SoloSalidas.txt ---\n"
  vuelos_para_asignar = []
  try:
      with open("SoloSalidas.txt", "r", encoding="utf-8") as f:
          lineas = f.readlines()
      if len(lineas) > 1:
          i = 1
          while i < len(lineas):
              partes = lineas[i].split()
              if len(partes) == 6:
                  id_vuelo = partes[0]
                  company = partes[1]
                  destino = partes[4]
                  hora_salida = partes[5]
                  nuevo_avion = Aircraft(id_vuelo, company, destino, "", destino, hora_salida)
                  vuelos_para_asignar.append(nuevo_avion)
              i += 1
  except FileNotFoundError:
      texto_salida += "Error: No se pudo leer SoloSalidas.txt. Asegúrate de haberlo creado primero.\n"

  res_night = AssignNightGates(aeropuerto, vuelos_para_asignar)
  texto_salida += f"Resultado de AssignNightGates: {res_night} (0 es éxito)\n"

  reporte_puertas = []
  for t in aeropuerto.terminal:
      for area in t.BoardingArea:
          for puerta in area.list:
              nombre = puerta.Gate_name
              ocupada = puerta.Gate_occupancy
              id_avion = puerta.Gate_aircraft_id if ocupada else ""
              hora = "-"
              if ocupada:
                  for a in vuelos_para_asignar:
                      if a.id == id_avion: hora = a.departure_time
              reporte_puertas.append((nombre, ocupada, id_avion, hora))

  texto_salida += "\n--- ESTADO DE LAS PUERTAS TRAS ASIGNAR VUELOS NOCTURNOS ---\n"
  ocupados = 0
  for nombre, ocupada, avion, hora in reporte_puertas:
      if ocupada:
          ocupados += 1
          texto_salida += f"Puerta: {nombre} | ESTADO: Ocupada | Vuelo: {avion} | Salida: {hora}\n"

  texto_salida += f"Total de puertas ocupadas por vuelos nocturnos: {ocupados}\n"
  mostrar_en_pantalla(texto_salida)

def MergeFiles():
  # 1. Pedir archivo de llegadas
  ruta_arrivals = filedialog.askopenfilename(title="1. Selecciona el archivo de llegadas",
                                             filetypes=[("Archivos de texto", "*.txt"),
                                                        ("Todos los archivos", "*.*")])
  if not ruta_arrivals:
      mostrar_en_pantalla("⚠️ Operación cancelada: No se seleccionó el archivo de llegadas.")
      return

  # 2. Pedir archivo de salidas
  ruta_departures = filedialog.askopenfilename(title="2. Selecciona el archivo de salidas",
                                               filetypes=[("Archivos de texto", "*.txt"),
                                                          ("Todos los archivos", "*.*")])
  if not ruta_departures:
      mostrar_en_pantalla("⚠️ Operación cancelada: No se seleccionó el archivo de salidas.")
      return

  try:
      # Cargar los archivos usando las rutas seleccionadas
      arrivals2 = LoadArrivals(ruta_arrivals)
      departures = LoadDepartures(ruta_departures)

      texto_salida = f"Archivos cargados:\n- Llegadas: {len(arrivals2)}\n- Salidas: {len(departures)}\n"

      if len(departures) > 0:
          texto_salida += f"Primer departure: id={departures[0].id} destino={departures[0].destination} hora={departures[0].departure_time}\n"

      # Fusionar
      merged = MergeMovements(arrivals2, departures)

      if merged != -1:
          texto_salida += f"\nMerged total: {len(merged)}\n"

          # Archivo general con todos los datos fusionados
          SaveMergedFlights(merged, "MergedFlights.txt")
          texto_salida += "✅ Archivo 'MergedFlights.txt' creado con éxito.\n"

          # Estadísticas y filtrado
          completos = [a for a in merged if a.origin != "" and a.destination != ""]
          solo_llegada = [a for a in merged if a.origin != "" and a.destination == ""]
          solo_salida = [a for a in merged if a.origin == "" and a.departure_time != ""]

          # GENERACIÓN DEL ARCHIVO SOLOSALIDAS.TXT
          SaveMergedFlights(solo_salida, "SoloSalidas.txt")
          texto_salida += "✅ Archivo 'SoloSalidas.txt' creado con éxito.\n\n"

          texto_salida += f"-> Con llegada y salida: {len(completos)}\n"
          texto_salida += f"-> Solo llegada: {len(solo_llegada)}\n"
          texto_salida += f"-> Solo salida (nocturnos): {len(solo_salida)}\n"
      else:
          texto_salida += "\n❌ Error en la fusión de los movimientos (MergeMovements devolvió -1)."

      # Mostrar resultados en la consola de la interfaz
      mostrar_en_pantalla(texto_salida)

  except Exception as e:
      mostrar_en_pantalla(f"❌ Error al procesar los archivos:\n{e}")

def RunTestFreeGate():
  id_test_liberar = simpledialog.askstring("Liberar Puerta", "Introduce el ID del aircraft que deseas liberar:",
                                           parent=window)
  if not id_test_liberar:
      mostrar_en_pantalla("Operación cancelada por el usuario.")
      return

  texto_salida = f"\n--- TEST: FreeGate ---\nID a liberar: {id_test_liberar}\n"

  # 1. Liberar la puerta en la memoria del aeropuerto global
  res_liberar = FreeGate(aeropuerto, id_test_liberar)

  if res_liberar == 0:
      texto_salida += f" -> ¡Éxito! El avión '{id_test_liberar}' ha sido retirado de su puerta en memoria.\n"
  else:
      texto_salida += f" -> Error ({res_liberar}): No se encontró ningún avión con el ID '{id_test_liberar}' en la estructura actual.\n"

  # 2. Eliminar el avión de los archivos físicos
  archivos_a_modificar = ["SoloSalidas.txt", "MergedFlights.txt"]
  for archivo in archivos_a_modificar:
      try:
          if not os.path.exists(archivo):
              continue

          with open(archivo, "r", encoding="utf-8") as f:
              lineas = f.readlines()

          if lineas:
              cabecera = lineas[0]
              vuelos_restantes = []
              eliminado_del_archivo = False

              for linea in lineas[1:]:
                  partes = linea.split()
                  # Si la línea tiene contenido y el ID coincide, la saltamos (eliminamos)
                  if partes and partes[0] == id_test_liberar:
                      eliminado_del_archivo = True
                  else:
                      vuelos_restantes.append(linea)

              if eliminado_del_archivo:
                  with open(archivo, "w", encoding="utf-8") as f:
                      f.write(cabecera)
                      f.writelines(vuelos_restantes)
                  texto_salida += f" -> ✅ Vuelo eliminado de '{archivo}'.\n"
              else:
                  texto_salida += f" -> ⚠️ El ID no figuraba en '{archivo}'.\n"

      except Exception as e:
          texto_salida += f" -> ❌ Error al procesar '{archivo}': {e}\n"

  # 3. Comprobación de las puertas que quedan
  try:
      ocupados_tras_free = [p for p in GateOccupancy(aeropuerto) if p[1] == True]
      texto_salida += f"\nPuertas que permanecen ocupadas en tiempo real: {len(ocupados_tras_free)}\n"
  except Exception:
      pass

  mostrar_en_pantalla(texto_salida)

def ContarPuertasOcupadasTerminal():    #nueva función del examen
  frame_grafico.pack_forget()
  frame_mapa.pack_forget()
  frame_texto.pack(fill=BOTH, expand=True)

  for widget in frame_texto.winfo_children():
      if widget != area_resultado:
          widget.destroy()

  area_resultado.pack_forget()

  frame_input = Frame(frame_texto, pady=10)
  frame_input.pack(fill=X)

  Label(frame_input, text="Introduce terminal (ej. T1 o T2):", font=("Arial", 11, "bold")).pack(side=LEFT, padx=5)

  entry_terminal = Entry(frame_input, font=("Arial", 11), width=15)
  entry_terminal.pack(side=LEFT, padx=5)
  entry_terminal.focus_set()

  def procesar_terminal():
      global aeropuerto
      nombre_terminal = entry_terminal.get().strip().upper()
# INTRODUCE EL NOMBRE DE LA TERMINAL
      if nombre_terminal == "":
          mostrar_en_pantalla("⚠️ No has introducido ningún identificador de terminal.")
          return
      contador_ocupadas = 0
      terminal_encontrada = False
      i = 0
      while i < len(aeropuerto.terminal):
          terminal_actual = aeropuerto.terminal[i]
          if terminal_actual.name.upper() == nombre_terminal:
              terminal_encontrada = True
              j = 0
              while j < len(terminal_actual.BoardingArea):
                  area_actual = terminal_actual.BoardingArea[j]
                  k = 0
                  while k < len(area_actual.list):
                      puerta_actual = area_actual.list[k]
                      if puerta_actual.Gate_occupancy == True:
                          contador_ocupadas = contador_ocupadas + 1
                      k = k + 1
                  j = j + 1
          i = i + 1

      if terminal_encontrada == False:
          mostrar_en_pantalla("❌ No existe la terminal '" + nombre_terminal + "' en el aeropuerto.")
      else:
          mostrar_en_pantalla(
              "Terminal consultada: " + nombre_terminal + "\n"
              "Puertas ocupadas actualmente: " + str(contador_ocupadas)
          )

  Button(frame_input, text="Contar puertas ocupadas", bg="#16a085", fg="white",
         font=("Arial", 10, "bold"), command=procesar_terminal).pack(side=LEFT, padx=10)

  area_resultado.pack(fill=BOTH, expand=True)

  area_resultado.config(state="normal")
  area_resultado.delete("1.0", END)
  area_resultado.insert(END, "Introduce una terminal arriba y pulsa el botón.\n")
  area_resultado.config(state="disabled")

def PanelSimulacionHoraria():
  aeropuerto_sim = LoadAirportStructure("Terminals.txt")
  lista_vuelos_dia = []
  try:
      with open("MergedFlights.txt", "r", encoding="utf-8") as f:
          lineas = f.readlines()
      if len(lineas) > 1:
          i = 1
          while i < len(lineas):
              partes = lineas[i].split()
              if len(partes) == 6:
                  llegada = "" if partes[3] == "-" else partes[3]
                  salida = "" if partes[5] == "-" else partes[5]
                  nuevo_avion = Aircraft(partes[0], partes[1], partes[2], llegada, partes[4], salida)
                  lista_vuelos_dia.append(nuevo_avion)
              i += 1
  except FileNotFoundError:
      mostrar_en_pantalla("❌ Error: No se pudo encontrar el archivo MergedFlights.txt.")
      return

  for avion in lista_vuelos_dia:
      avion.real_departure = avion.departure_time
      if avion.departure_time != "":
          partes_h = avion.departure_time.split(":")
          hh = int(partes_h[0])
          mm = int(partes_h[1])
          if mm > 0:
              avion.departure_time = f"{hh + 1:02d}:00"

  puertas = []
  try:
      for t in aeropuerto_sim.terminal:
          for ar in t.BoardingArea:
              puertas.extend(ar.list)
  except:
      pass

  if not puertas:
      mostrar_en_pantalla("❌ No hay puertas en memoria.")
      return

  puertas_por_zona = {}
  for p in puertas:
      zona, num = extraer_zona_num(p.Gate_name)
      if zona not in puertas_por_zona: puertas_por_zona[zona] = []
      puertas_por_zona[zona].append((num, p))
  zonas_ordenadas = sorted(list(puertas_por_zona.keys()))

  for widget in frame_menu_s.winfo_children(): widget.destroy()

  Label(frame_menu_s, text="Panel de Simulación Diaria", font=("Courier", 16, "bold")).pack(pady=(10, 5))
  hora_actual_var = StringVar(value="00:00")
  zona_actual_var = StringVar(value="")

  def mostrar_mapa_zona_simulacion(zona, lista_p_tuplas):
      try:
          plt.clf()
          plt.close('all')
          alto_figura = max(6, len(lista_p_tuplas) // 2.5)
          fig = plt.figure(figsize=(7, alto_figura), facecolor='white')
          ax = fig.add_subplot(111)


          lista_p_ordenada = sorted(lista_p_tuplas, key=lambda x: x[0])
          y_spine, x_zone = 0, 0
          num_niveles = (len(lista_p_ordenada) + 1) // 2
          y_bottom = y_spine - 2 - (num_niveles * 2)

          ax.plot([x_zone, x_zone], [y_spine, y_bottom], color='#2c3e50', linewidth=8, zorder=1)
          ax.text(x_zone, y_spine + 1, f"Muelle {zona} - {hora_actual_var.get()}", fontsize=14, fontweight='bold',
                  va='bottom', ha='center', color="#2c3e50")

          estado_en_vivo = {}
          try:
              for nombre, est, avion in GateOccupancy(aeropuerto_sim):
                  estado_en_vivo[nombre] = (est, avion)
          except Exception:
              pass

          for idx_p, (num_g, p) in enumerate(lista_p_ordenada):
              nivel = idx_p // 2
              y_gate = y_spine - 2 - (nivel * 2)
              es_derecha = True
              try:
                  es_derecha = (int(num_g) % 2 != 0)
              except:
                  pass

              if es_derecha:
                  x_start, x_end = x_zone, x_zone + 2
                  ha_text, x_text = 'left', x_end + 0.5
              else:
                  x_start, x_end = x_zone, x_zone - 2
                  ha_text, x_text = 'right', x_end - 0.5


              ax.plot([x_start, x_end], [y_gate, y_gate], color='#34495e', linewidth=4, zorder=1)

              nombre_puerta = p.Gate_name if hasattr(p, 'Gate_name') else f"{zona}G{num_g}"
              ocupada, avion_asignado = estado_en_vivo.get(nombre_puerta, (False, None))

              color_cuadrado = '#e74c3c' if ocupada else '#2ecc71'
              ax.plot(x_end, y_gate, marker='s', color=color_cuadrado, markersize=14, zorder=2)

              if ocupada and avion_asignado:
                  texto_puerta = getattr(avion_asignado, 'id', str(avion_asignado))
                  color_texto = '#c0392b'
              else:
                  texto_puerta = nombre_puerta
                  color_texto = '#27ae60'

              ax.text(x_text, y_gate, texto_puerta, fontsize=10, fontweight='bold', va='center', ha=ha_text,
                      color=color_texto)

          ax.set_xlim(-6, 6)
          ax.set_ylim(y_bottom - 2, y_spine + 3)
          ax.axis('off')
          plt.tight_layout()
          mostrar_grafico_en_pantalla()
      except Exception as e:
          mostrar_en_pantalla(f"❌ Excepción gráfica atrapada al dibujar {zona}: {e}")

  def resetear_puertas(aeropuerto):
      for t in aeropuerto.terminal:
          for ar in t.BoardingArea:
              for p in ar.list:
                  p.Gate_occupancy = False
                  if hasattr(p, 'Gate_aircraft_id'): p.Gate_aircraft_id = ""
                  if hasattr(p, 'Gate_aircraft'): p.Gate_aircraft = None

  def seleccionar_hora(h):
      hora_actual_var.set(h)
      resetear_puertas(aeropuerto_sim)
      AssignGatesAtTime(aeropuerto_sim, lista_vuelos_dia, h)
      zona = zona_actual_var.get()
      if zona:
          mostrar_en_pantalla(f"🕒 Periodo actualizado a: {h}\nMostrando mapa del Muelle {zona}.\n")
          mostrar_mapa_zona_simulacion(zona, puertas_por_zona[zona])
      else:
          mostrar_en_pantalla(f"🕒 Periodo actualizado a: {h}\nSelecciona un Muelle abajo.")

  def seleccionar_zona(z):
      zona_actual_var.set(z)
      h = hora_actual_var.get()
      mostrar_en_pantalla(f"🕒 Periodo actualizado a: {h}\nMostrando mapa del Muelle {z}.\n")
      mostrar_mapa_zona_simulacion(z, puertas_por_zona[z])

  Label(frame_menu_s, text="1. Selecciona el Periodo:", font=("Arial", 11, "bold")).pack(pady=(5, 0))
  frame_horas = Frame(frame_menu_s, bg="#ecf0f1", padx=5, pady=5)
  frame_horas.pack(fill=X, padx=10, pady=5)
  for c in range(6): frame_horas.columnconfigure(c, weight=1)

  row, col = 0, 0
  for h in range(24):
      hora_str = f"{h:02d}:00"
      btn_h = Button(frame_horas, text=hora_str, font=("Arial", 9), bg="#bdc3c7",
                     command=lambda hora=hora_str: seleccionar_hora(hora))
      btn_h.grid(row=row, column=col, padx=2, pady=2, sticky=NSEW)
      col += 1
      if col > 5:
          col = 0
          row += 1

  Label(frame_menu_s, text="2. Selecciona el Muelle a visualizar:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
  frame_botones_zonas = Frame(frame_menu_s)
  frame_botones_zonas.pack(fill=BOTH, expand=True, padx=10, pady=5)
  for c in range(3): frame_botones_zonas.columnconfigure(c, weight=1)

  row, col = 0, 0
  for zona in zonas_ordenadas:
      btn_z = Button(frame_botones_zonas, text=f"Muelle {zona}", font=("Arial", 10, "bold"), bg="#2980b9", fg="white",
                     command=lambda z=zona: seleccionar_zona(z))
      btn_z.grid(row=row, column=col, padx=5, pady=5, sticky=NSEW, ipady=8)
      col += 1
      if col > 2:
          col = 0
          row += 1

  Label(frame_menu_s, text="3. Consultar Ocupación por Terminal:", font=("Arial", 11, "bold")).pack(pady=(15, 0))
  frame_consulta_term = Frame(frame_menu_s, pady=5)
  frame_consulta_term.pack(fill=X, padx=10)

  Label(frame_consulta_term, text="Terminal:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=(5, 2))
  entry_terminal = Entry(frame_consulta_term, font=("Arial", 11), width=8, justify="center")
  entry_terminal.insert(0, "T1")
  entry_terminal.pack(side=LEFT, padx=5)

  def calcular_puertas_terminal():
      term = entry_terminal.get().strip().upper()
      if term not in ["T1", "T2"]:
          mostrar_en_pantalla("⚠️ Error: Introduce 'T1' o 'T2' en el cuadro de texto para calcular.")
          return

      hora_act = hora_actual_var.get()

      zonas_t1 = ["A", "B", "C", "D", "E"]
      zonas_t2 = ["M", "R", "S", "U", "W", "Y"]

      puertas_ocupadas = 0
      total_puertas = 0
      detalles_lista = []


      try:
          for nombre, est, avion in GateOccupancy(aeropuerto_sim):
              zona_p, num_p = extraer_zona_num(nombre)
              zona_p_upper = zona_p.upper()


              pertenece = False


              if term == "T1":
                  if zona_p_upper.startswith("T1") or any(z in zona_p_upper for z in zonas_t1):
                      pertenece = True


              elif term == "T2":
                  if zona_p_upper.startswith("T2") or any(z in zona_p_upper for z in zonas_t2):
                      pertenece = True


              if pertenece:
                  total_puertas = total_puertas + 1


                  if est:
                      puertas_ocupadas = puertas_ocupadas + 1
                      detalles_lista.append("  • Puerta: " + str(nombre) + " ➔ Vuelo: " + str(avion))


          texto_reporte = (
                  "REPORTE DE OCUPACIÓN EN TIEMPO REAL\n"
                  "----------------------------------------\n"
                  "Terminal seleccionada : Terminal " + term + "\n"
                                                               "Periodo de simulación : " + hora_act + "\n"
                                                                                                       "Total de puertas      : " + str(
              total_puertas) + "\n"
                               "Puertas ocupadas      : " + str(puertas_ocupadas) + "\n"
                                                                                    "Puertas disponibles   : " + str(
              total_puertas - puertas_ocupadas) + "\n"
                                                  "----------------------------------------\n"
          )


          if len(detalles_lista) > 0:
              texto_reporte = texto_reporte + "Detalle de puertas ocupadas:\n" + "\n".join(detalles_lista)
          else:
              texto_reporte = texto_reporte + "No hay aeronaves estacionadas en esta terminal a esta hora."


          mostrar_en_pantalla(texto_reporte)


      except Exception as err:
          mostrar_en_pantalla("❌ Error al procesar la ocupación de la terminal: " + str(err))


  btn_calcular = Button(frame_consulta_term, text="Calcular Puertas", bg="#27ae60", fg="white",
                        font=("Arial", 9, "bold"), command=calcular_puertas_terminal)
  btn_calcular.pack(side=LEFT, padx=5)


  Button(frame_menu_s, text="⬅ Volver Atrás", bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
         command=lambda: mostrar_menu(frame_menu_3)).pack(pady=10, ipady=8, fill=X, padx=10)
  mostrar_en_pantalla(
      f"✅ Panel unificado cargado exitosamente.\nHay {len(lista_vuelos_dia)} vuelos cargados.\n\n-> Paso 1: Haz clic en una hora.\n-> Paso 2: Haz clic en un Muelle para visualizar el estado.")
  mostrar_menu(frame_menu_s)

def RunTestPlotDay():
  plt.close('all')
  plt.figure(figsize=(10, 6))
  aeropuerto_diario = LoadAirportStructure("Terminals.txt")
  lista_vuelos_dia = []
  try:
      with open("MergedFlights.txt", "r", encoding="utf-8") as f:
          lineas = f.readlines()
      if len(lineas) > 1:
          i = 1
          while i < len(lineas):
              partes = lineas[i].split()
              if len(partes) == 6:
                  llegada = "" if partes[3] == "-" else partes[3]
                  salida = "" if partes[5] == "-" else partes[5]
                  nuevo_avion = Aircraft(partes[0], partes[1], partes[2], llegada, partes[4], salida)
                  lista_vuelos_dia.append(nuevo_avion)
              i += 1
  except FileNotFoundError:
      mostrar_en_pantalla("Error: No se pudo encontrar el archivo MergedFlights.txt")
      return

  for avion in lista_vuelos_dia:
      avion.real_departure = avion.departure_time
      if avion.departure_time != "":
          partes_h = avion.departure_time.split(":")
          if int(partes_h[1]) > 0: avion.departure_time = f"{int(partes_h[0]) + 1:02d}:00"

  PlotDayOccupancy(aeropuerto_diario, lista_vuelos_dia)
  mostrar_grafico_en_pantalla()


# DISEÑO DE LOS MENÚS PRINCIPALES
Label(frame_menu_principal, text="Menú principal", font=("Courier", 24, "bold")).pack(pady=(50, 30))
Button(frame_menu_principal, text="1. Funciones para cargar los vuelos", font=("Arial", 14), bg="#4caf50", fg="white",
     command=lambda: mostrar_menu(frame_menu_1)).pack(fill=X, padx=50, pady=10, ipady=10)
Button(frame_menu_principal, text="2. Funciones para ver los vuelos", font=("Arial", 14), bg="#2196f3", fg="white",
     command=lambda: mostrar_menu(frame_menu_2)).pack(fill=X, padx=50, pady=10, ipady=10)
Button(frame_menu_principal, text="3. Funciones del aeropuerto LEBL", font=("Arial", 14), bg="#8e44ad", fg="white",
     command=lambda: mostrar_menu(frame_menu_3)).pack(fill=X, padx=50, pady=10, ipady=10)

# MENÚ 1
Label(frame_menu_1, text="1. Menú Cargar Vuelos", font=("Courier", 18, "italic")).grid(row=0, column=0, columnspan=4,
                                                                                     pady=(10, 20))
for r in range(4): frame_menu_1.rowconfigure(r, weight=1)
for c in range(4): frame_menu_1.columnconfigure(c, weight=1)
Button(frame_menu_1, text="Establecer vuelos Schengen", bg="orange", command=AClick).grid(row=1, column=0, padx=5,
                                                                                        pady=5, sticky=NSEW)
Button(frame_menu_1, text="Clasificar aeropuerto", bg="orange", command=BClick).grid(row=1, column=1, padx=5, pady=5,
                                                                                   sticky=NSEW)
Button(frame_menu_1, text="Cargar todos los aeropuertos", bg="orange", command=CClick).grid(row=1, column=2, padx=5,
                                                                                          pady=5, sticky=NSEW)
Button(frame_menu_1, text="Añadir aeropuerto", bg="orange", command=DClick).grid(row=1, column=3, padx=5, pady=5,
                                                                               sticky=NSEW)
Button(frame_menu_1, text="Eliminar aeropuerto", bg="orange", command=EClick).grid(row=2, column=0, padx=5, pady=5,
                                                                                 sticky=NSEW)
Button(frame_menu_1, text="Guardar aeropuertos por zona", bg="orange", command=FClick).grid(row=2, column=1, padx=5,
                                                                                          pady=5, sticky=NSEW)
Button(frame_menu_1, text="Mostrar cantidad aeropuertos por zona", bg="orange", command=GClick).grid(row=2, column=2,
                                                                                                   padx=5, pady=5,
                                                                                                   sticky=NSEW)
Button(frame_menu_1, text="Ubicacion de los aeropuertos", bg="orange", command=HClick).grid(row=2, column=3, padx=5,
                                                                                          pady=5, sticky=NSEW)
Button(frame_menu_1, text="⬅ Volver al Menú Principal", bg="#e0e0e0", font=("Arial", 11, "bold"),
     command=lambda: mostrar_menu(frame_menu_principal)).grid(row=3, column=0, columnspan=4, pady=20, ipady=5,
                                                              sticky=EW)

# MENÚ 2
Label(frame_menu_2, text="2. Gestión de Llegadas y Vuelos", font=("Courier", 18, "italic")).grid(row=0, column=0,
                                                                                               columnspan=4,
                                                                                               pady=(10, 20))
for r in range(4): frame_menu_2.rowconfigure(r, weight=1)
for c in range(4): frame_menu_2.columnconfigure(c, weight=1)
Button(frame_menu_2, text="Abrir archivo arrivals", bg="orange", command=IClick).grid(row=1, column=0, padx=5, pady=5,
                                                                                    sticky=NSEW)
Button(frame_menu_2, text="Vuelos llegados por hora", bg="orange", command=JClick).grid(row=1, column=1, padx=5, pady=5,
                                                                                      sticky=NSEW)
Button(frame_menu_2, text="Crear archivo Flights.txt", bg="orange", command=KClick).grid(row=1, column=2, padx=5,
                                                                                       pady=5, sticky=NSEW)
Button(frame_menu_2, text="Gráfico de vuelos por aerolinea", bg="orange", command=LClick).grid(row=1, column=3, padx=5,
                                                                                             pady=5, sticky=NSEW)
Button(frame_menu_2, text="Tipos de vuelos", bg="orange", command=MClick).grid(row=2, column=0, padx=5, pady=5,
                                                                             sticky=NSEW)
Button(frame_menu_2, text="Mapa de trayectoria de vuelos", bg="orange", command=NClick).grid(row=2, column=1, padx=5,
                                                                                           pady=5, sticky=NSEW)
Button(frame_menu_2, text="Vuelos largos", bg="orange", command=OClick).grid(row=2, column=2, padx=5, pady=5,
                                                                           sticky=NSEW)
Button(frame_menu_2, text="⬅ Volver al Menú Principal", bg="#e0e0e0", font=("Arial", 11, "bold"),
     command=lambda: mostrar_menu(frame_menu_principal)).grid(row=3, column=0, columnspan=4, pady=20, ipady=5,
                                                              sticky=EW)


# MENÚ 3
Label(frame_menu_3, text="3. Aeropuerto LEBL", font=("Courier", 18, "italic")).grid(row=0, column=0, columnspan=4,
                                                                                    pady=(10, 20))
for r in range(6): frame_menu_3.rowconfigure(r, weight=1)   #CAMBIAR PORQUE HEMOS AÑADIDO UN BOTÓN
for c in range(4): frame_menu_3.columnconfigure(c, weight=1)
Button(frame_menu_3, text="Crear Puertas", bg="#9b59b6", fg="white", command=RunTest1).grid(row=1, column=0, padx=5,
                                                                                          pady=5, sticky=NSEW)
Button(frame_menu_3, text="Cargar Aerolineas", bg="#9b59b6", fg="white", command=RunTest2).grid(row=1, column=1, padx=5,
                                                                                              pady=5, sticky=NSEW)
Button(frame_menu_3, text="Cargar Aeropuerto", bg="#9b59b6", fg="white", command=RunTest3).grid(row=1, column=2, padx=5,
                                                                                              pady=5, sticky=NSEW)
Button(frame_menu_3, text="Crear archivo de vuelos", bg="#27ae60", fg="white", command=MergeFiles).grid(row=1, column=3,
                                                                                                      padx=5, pady=5,
                                                                                                      sticky=NSEW)
Button(frame_menu_3, text="Está en terminal", bg="#9b59b6", fg="white", command=RunTest5).grid(row=2, column=0, padx=5,
                                                                                             pady=5, sticky=NSEW)
Button(frame_menu_3, text="Buscar en terminal", bg="#9b59b6", fg="white", command=RunTest6).grid(row=2, column=1,
                                                                                               padx=5, pady=5,
                                                                                               sticky=NSEW)
Button(frame_menu_3, text="Ocupar puertas solo vuelos de noche", bg="#9b59b6", fg="white",
     command=RunTestNightGates).grid(row=2, column=2, padx=5, pady=5, sticky=NSEW)
Button(frame_menu_3, text="Eliminar un vuelo", bg="#9b59b6", fg="white", command=RunTestFreeGate).grid(row=2, column=3,
                                                                                                     padx=5, pady=5,
                                                                                                     sticky=NSEW)
Button(frame_menu_3, text="Mapa gráfico del aeropuerto interactivo", bg="#f1c40f", fg="black",
     font=("Arial", 10, "bold"), command=PanelSimulacionHoraria).grid(row=3, column=0, columnspan=2, padx=5, pady=5,
                                                                      sticky=NSEW)
Button(frame_menu_3, text="Gráfico de vuelos por hora", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
     command=RunTestPlotDay).grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
Button(frame_menu_3, text="⬅ Volver al Menú Principal", bg="#e0e0e0", font=("Arial", 11, "bold"),
     command=lambda: mostrar_menu(frame_menu_principal)).grid(row=5, column=0, columnspan=4, pady=20, ipady=5,
                                                              sticky=EW)
Button(frame_menu_3, text="Contar gates ocupadas por terminal", bg="#16a085", fg="white",
     font=("Arial", 10, "bold"), command=ContarPuertasOcupadasTerminal).grid(row=4, column=0, columnspan=2,
                                                                            padx=5, pady=5, sticky=NSEW)

# CIERRE SEGURO DE LA APLICACIÓN
def on_closing():
  """Manejador para cerrar la aplicación sin dejar tareas colgadas en segundo plano."""
  try:
      plt.close('all')  # Libera la memoria de todas las figuras de Matplotlib
  except:
      pass
  window.quit()  # Detiene el bucle principal (mainloop) de forma ordenada
  window.destroy()  # Destruye la ventana y el intérprete Tcl de forma segura

# Interceptamos el clic en la "X" de la ventana para que use nuestra función
window.protocol("WM_DELETE_WINDOW", on_closing)

# INICIALIZACIÓN FINAL
mostrar_menu(frame_menu_principal)
window.mainloop()
