class BarcelonaAP:
  def __init__(self, BarcelonaAP_code, BarcelonaAP_terminal):
      self.code = BarcelonaAP_code
      self.terminal = BarcelonaAP_terminal
class Terminal:
  def __init__(self, Terminal_name, Terminal_BoardingArea, Terminal_Icao):
      self.name = Terminal_name
      self.BoardingArea = Terminal_BoardingArea
      self.Icao = Terminal_Icao  # Nombre correcto
class BoardingArea:
  def __init__(self, BoardingArea_name, BoardingArea_type, BoardingArea_list):
      self.name = BoardingArea_name
      self.type = BoardingArea_type
      self.list = BoardingArea_list
class Gate:
  def __init__(self, Gate_name, Gate_occupancy, Gate_aircraft_id):
      self.Gate_name = Gate_name
      self.Gate_occupancy = Gate_occupancy
      self.Gate_aircraft_id = Gate_aircraft_id

#Función 1
def SetGates(area, init_gate, end_gate, prefix):
  if end_gate <= init_gate:
      return -1
  area.list = []
  for gate_number in range(init_gate, end_gate + 1):
      gate_name = prefix + str(gate_number)
      # Creamos el objeto Gate con los 3 valores
      new_gate = Gate(gate_name, False, "")
      area.list.append(new_gate)

#Función 2
def LoadAirlines(terminal, t_name):
  filename = t_name + "_Airlines.txt"
  try:
      with open(filename, 'r') as file:
          new_icao_list = []
          line = file.readline()
          while line != "":
              if line[-1] == '\n':
                  line = line[:-1]
              line_data = line.split('\t')
              if len(line_data) >= 2:
                  icao_code = line_data[1]
                  new_icao_list.append(icao_code)
              line = file.readline()
  except FileNotFoundError:
      return -1
  terminal.Icao = new_icao_list # Antes decía icao_codes
  return 0

#Función 3
def LoadAirportStructure(filename):
  try:
      file = open(filename, 'r')
  except FileNotFoundError:
      return -1
  # Primera línea: Código ICAO y número de terminales
  line = file.readline()
  if line != "" and line[-1] == '\n':
      line = line[:-1]
  data = line.split()
  airport_code = data[0]
  num_terminals = int(data[1])
  # Usamos self.code y self.terminal (lista) de BarcelonaAP
  airport = BarcelonaAP(airport_code, [])
  terminal_count = 0
  while terminal_count < num_terminals:
      # Leemos cabecera de terminal: nombre y número de áreas
      line = file.readline()
      if line != "" and line[-1] == '\n':
          line = line[:-1]
      data = line.split()
      term_name = data[1]
      num_areas = int(data[2])
      # Usamos self.name, self.BoardingArea (lista) y self.Icao (lista)
      terminal = Terminal(term_name, [], [])
      # Carga las aerolíneas en terminal.Icao
      LoadAirlines(terminal, term_name)
      area_count = 0
      while area_count < num_areas:
          # Datos del área de embarque
          line = file.readline()
          if line != "" and line[-1] == '\n':
              line = line[:-1]
          data = line.split()
          area_name = data[1]
          area_type = data[2]
          init_gate = int(data[4])
          end_gate = int(data[6])
          # Usamos self.name, self.type y self.list (lista de puertas)
          area = BoardingArea(area_name, area_type, [])
          # Prefijo para SetGates (ej: T1BAaG)
          prefix = area_name + "G"
          SetGates(area, init_gate, end_gate, prefix)
          # Añadimos a la lista 'BoardingArea' de la Terminal
          terminal.BoardingArea.append(area)
          area_count += 1
      # Añadimos a la lista 'terminal' del BarcelonaAP
      airport.terminal.append(terminal)
      terminal_count += 1
  file.close()
  return airport

#Función 4:
def GateOccupancy(bcn):
  # Creamos la lista vacía donde guardaremos los resultados
  resultado = []
  # Entramos en las terminales
  for t in bcn.terminal:
      # Entramos en las áreas de embarque de la terminal
      for area in t.BoardingArea:
          # Entramos en la lista de puertas del área
          for puerta in area.list:
              # Sacamos el nombre y el estado (booleano)
              nombre = puerta.Gate_name
              ocupada = puerta.Gate_occupancy
              # Obtenemos el ID del avión si la puerta está ocupada
              if ocupada == True:
                  avion = puerta.Gate_aircraft_id
              else:
                  avion = ""
              # Creamos el paquete de datos (tupla)
              datos_puerta = (nombre, ocupada, avion)
              # Lo guardamos en nuestra lista
              resultado.append(datos_puerta)
  # Al final devolvemos toda la lista llena
  return resultado

#Función 5:
def IsAirlineInTerminal(terminal, name):
  if name == "":
      return False
  lista_aerolineas = terminal.Icao
  if lista_aerolineas == []:
      return False
  i = 0
  encontrado = False
  while i < len(lista_aerolineas):
      if lista_aerolineas[i] == name:
          encontrado = True
      i = i + 1
  return encontrado

#Función 6:
def SearchTerminal(bcn, name):
  # Empezamos con un string vacío por si no encontramos la aerolínea
  nombre_terminal_encontrada = ""
  # Obtenemos la lista de terminales del aeropuerto
  lista_t = bcn.terminal
  # Recorremos la lista de terminales con un while
  i = 0
  total_terminales = len(lista_t)
  while i < total_terminales:
      terminal_actual = lista_t[i]
      # Llamamos a la Función 5 asumiendo que devuelve True o False
      encontrada = IsAirlineInTerminal(terminal_actual, name)
      # Si la aerolínea está en esta terminal
      if encontrada == True:
          # Guardamos el nombre de la terminal (usando .name de la clase Terminal)
          nombre_terminal_encontrada = terminal_actual.name
      i = i + 1
  # Devolvemos el nombre hallado o "" si no estaba en ninguna terminal
  return nombre_terminal_encontrada

def AssignGate(bcn, aircraft):
  # Primero obtenemos los datos del avión
  id_avion = aircraft.aircraft_id
  aerolinea_avion = aircraft.airline_icao
  tipo_vuelo_avion = aircraft.flight_type  # "Schengen" o "non-Schengen"
  # Después buscamos en qué terminal debe estar esta aerolínea
  # Usamos la Función 6
  nombre_terminal_correcta = SearchTerminal(bcn, aerolinea_avion)
  # Si la aerolínea no está en ninguna terminal, devolvemos un error
  if nombre_terminal_correcta == "":
      return -1
  # Ahora recorremos el aeropuerto para encontrar esa terminal
  lista_t = bcn.terminal
  i = 0
  encontrado = False
  while i < len(lista_t):
      term = lista_t[i]
      # Si es la terminal que buscamos
      if term.name == nombre_terminal_correcta:
          # buscamos el área de embarque correcta dentro de la terminal
          lista_areas = term.BoardingArea
          j = 0
          while j < len(lista_areas):
              area = lista_areas[j]
              # Comprobamos si el tipo de área coincide con el tipo de vuelo
              if area.type == tipo_vuelo_avion:
                  # Buscamos la primera puerta libre en esta área
                  lista_puertas = area.list
                  k = 0
                  while k < len(lista_puertas):
                      puerta = lista_puertas[k]
                      # Si la puerta no está ocupada
                      if puerta.Gate_occupancy == False:
                          # Si la encontramos actualizamos el estqado de la puerta
                          puerta.Gate_occupancy = True
                          puerta.Gate_aircraft_id = id_avion
                          # Devolvemos 0 para indicar éxito y salimos de la función
                          return 0
                      k = k + 1
              j = j + 1
      i = i + 1
  # Si llegamos aquí es porque no había puertas libres del tipo correcto
  return -2
