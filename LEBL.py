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


# Función 1
def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1
    area.list = []
    for gate_number in range(init_gate, end_gate + 1):
        gate_name = prefix + str(gate_number)
        # Creamos el objeto Gate con los 3 valores
        new_gate = Gate(gate_name, False, "")
        area.list.append(new_gate)


# Función 2
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
    terminal.Icao = new_icao_list  # Antes decía icao_codes
    return 0


# Función 3
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


# Función 4:
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


# Función 5:
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


# Función 6:
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


# Función 7:
def AssignGate(bcn, aircraft):
    prefijos = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL',
                'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    if len(aircraft.origin) >= 2 and aircraft.origin[:2] in prefijos:
        tipo_vuelo_avion = "Schengen"
    else:
        tipo_vuelo_avion = "non-Schengen"
    # Primero obtenemos los datos del avión
    id_avion = aircraft.id
    aerolinea_avion = aircraft.company
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


# version 4 funcion 1 (Limpiada de clases externas)
def AssignNightGates(bcn, aircrafts):
    # Si la lista está vacía devolvemos error
    if len(aircrafts) == 0:
        return -1

    i = 0
    # Recorremos la lista de aviones que ya viene preparada desde el test
    while i < len(aircrafts):
        avion = aircrafts[i]

        # Intentamos asignar puerta a cada avión
        AssignGate(bcn, avion)

        i = i + 1

    return 0


# version 4 funcion 2
def FreeGate(bcn, id):
    # busca un aircraft dentro de todas las puertas del aeropuerto y libera la puerta donde está estacionado
    i = 0  # recorremos las terminales del aeropuerto
    while i < len(bcn.terminal):
        terminal_actual = bcn.terminal[i]
        j = 0  # ahora recorremos todas las áreas de embarque
        while j < len(terminal_actual.BoardingArea):
            area_actual = terminal_actual.BoardingArea[j]
            k = 0  # recorremos todas las puertas del área
            while k < len(area_actual.list):
                # comprobamos si esta puerta pertenece al aircraft que queremos liberar
                puerta_actual = area_actual.list[k]
                if puerta_actual.Gate_aircraft_id == id:
                    # la puerta deja de estar ocupada y borramos el id del avión
                    puerta_actual.Gate_occupancy = False
                    puerta_actual.Gate_aircraft_id = ""
                    return 0
                k = k + 1
            j = j + 1
        i = i + 1
    return -1


# version 4 funcion 3
def AssignGatesAtTime(bcn, aircrafts, time):
    # Calculamos el límite superior del intervalo de tiempo (1 hora más tarde)
    # Extraemos el número de la hora inicial, sumamos 1 y formateamos
    hora_inicio_int = int(time.split(":")[0])
    hora_fin_int = hora_inicio_int + 1
    time_end = f"{hora_fin_int:02d}:00"
    # primera fase: liberar las puertas de los aviones que despegan en este periodo
    i = 0
    while i < len(aircrafts):
        aircraft_actual = aircrafts[i]
        despegue = aircraft_actual.departure_time  # Usamos el nombre exacto de tu clase
        # Comprobamos si el despegue ocurre en el intervalo [time, time_end)
        if despegue != "" and time <= despegue < time_end:
            # Llamamos a tu Función FreeGate(bcn, id) pasándole el id exacto de tu clase (.id)
            FreeGate(bcn, aircraft_actual.id)
        i += 1
    # 3. SEGUNDA FASE: Asignar puertas a los aviones que aterrizan en este periodo
    unassigned_count = 0
    j = 0
    while j < len(aircrafts):
        aircraft_actual = aircrafts[j]
        aterrizaje = aircraft_actual.time_of_landing  # Usamos el nombre exacto de tu clase
        # Comprobamos si el aterrizaje ocurre en el intervalo [time, time_end)
        if aterrizaje != "" and time <= aterrizaje < time_end:
            # Intentamos asignarle puerta usando tu Función 7 (AssignGate)
            resultado_asignacion = AssignGate(bcn, aircraft_actual)
            # Si retorna -2 significa que no había puertas libres del tipo correcto
            if resultado_asignacion == -2:
                unassigned_count += 1
        j += 1
    # Devolvemos el número de aviones que se quedaron en tierra/espera sin puerta asignada
    return unassigned_count


# version 4 funcion 4
import matplotlib.pyplot as plt


def PlotDayOccupancy(bcn, aircrafts):
    # 1. Crear las estructuras para guardar los datos de las 24 horas
    horas_eje_x = []
    lista_no_asignados = []
    # Creamos un diccionario dinámico para guardar la ocupación de cada terminal.
    # Así funcionará independientemente de si tu aeropuerto tiene ["T1", "T2"] o más terminales.
    ocupacion_por_terminal = {}
    i = 0
    while i < len(bcn.terminal):
        nombre_terminal = bcn.terminal[i].name
        ocupacion_por_terminal[nombre_terminal] = [0] * 24  # Una lista de 24 ceros para cada terminal
        i += 1
    # 2. Simulación del día hora por hora (de 0 a 23)
    hora_int = 0
    while hora_int < 24:
        # Formateamos la hora actual en string de dos dígitos (ej: 0 -> "00:00", 14 -> "14:00")
        string_hora = f"{hora_int:02d}:00"
        horas_eje_x.append(string_hora)
        # LLAMADA CRÍTICA: Actualizamos el aeropuerto para esta hora y obtenemos los aviones sin puerta
        vuelos_sin_puerta = AssignGatesAtTime(bcn, aircrafts, string_hora)
        lista_no_asignados.append(vuelos_sin_puerta)
        # Ahora contamos cuántas puertas están ocupadas en este preciso instante en cada terminal
        t = 0
        while t < len(bcn.terminal):
            terminal_actual = bcn.terminal[t]
            contador_puertas_ocupadas = 0
            # Recorremos áreas de embarque de la terminal actual
            a = 0
            while a < len(terminal_actual.BoardingArea):
                area_actual = terminal_actual.BoardingArea[a]
                # Recorremos las puertas de esa área
                p = 0
                while p < len(area_actual.list):
                    puerta_actual = area_actual.list[p]
                    if puerta_actual.Gate_occupancy == True:
                        contador_puertas_ocupadas += 1
                    p += 1
                a += 1
            # Guardamos el total de puertas ocupadas en esta hora para esta terminal
            ocupacion_por_terminal[terminal_actual.name][hora_int] = contador_puertas_ocupadas
            t += 1
        hora_int += 1
    # 3. CONFIGURACIÓN Y GENERACIÓN DEL GRÁFICO
    plt.figure(figsize=(12, 6))
    # Dibujamos una línea para cada terminal del aeropuerto
    # Recorremos el diccionario de terminales con un bucle tradicional
    nombres_terminales = list(ocupacion_por_terminal.keys())
    k = 0
    while k < len(nombres_terminales):
        term_name = nombres_terminales[k]
        plt.plot(horas_eje_x, ocupacion_por_terminal[term_name], marker='o', linestyle='-',
                 label=f"Ocupación {term_name}")
        k += 1
    # Dibujamos la línea de aviones no asignados (fallos/retrasos por falta de sitio)
    plt.plot(horas_eje_x, lista_no_asignados, marker='x', color='red', linestyle='--', label="Aviones No Asignados")
    # Detalles estéticos del gráfico
    plt.title("Evolución de la ocupación de puertas y fallos a lo largo del día", fontsize=14)
    plt.xlabel("Periodo Horario", fontsize=12)
    plt.ylabel("Cantidad de aeronaves / puertas", fontsize=12)
    plt.xticks(rotation=45)  # Rotamos las horas para que se lean bien
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc="upper left")
    plt.tight_layout()  # Ajusta el gráfico para que no se corten las etiquetas de las horas
    # Mostramos el gráfico en pantalla
    plt.show()
