import random

TAM_MINIMO = 6
FLOTA = [1, 1, 2, 2, 3, 4]

# ============================================================
# LÓGICA DEL TABLERO
# ============================================================
def crear_tablero(n):
    tablero = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(".")
        tablero.append(fila)
    return tablero


def puede_colocar(tablero, fila, col, tamano, horizontal):
    n = len(tablero)

    if horizontal:
        if col + tamano > n:
            return False
        for i in range(tamano):
            if tablero[fila][col + i] != ".":
                return False
    else:
        if fila + tamano > n:
            return False
        for i in range(tamano):
            if tablero[fila + i][col] != ".":
                return False

    return True


def colocar_barco(tablero, fila, col, tamano, horizontal):
    barco = []

    for i in range(tamano):
        if horizontal:
            f = fila
            c = col + i
        else:
            f = fila + i
            c = col

        tablero[f][c] = "B"
        barco.append([f, c])

    return barco


def colocar_barcos(tablero, flota):
    n = len(tablero)
    barcos = []

    for tamano in flota:
        colocado = False

        while not colocado:
            fila = random.randint(0, n - 1)
            col = random.randint(0, n - 1)
            horizontal = random.randint(0, 1) == 0

            if puede_colocar(tablero, fila, col, tamano, horizontal):
                barco = colocar_barco(tablero, fila, col, tamano, horizontal)
                barcos.append(barco)
                colocado = True

    return barcos


# ============================================================
# LÓGICA DE DISPAROS
# ============================================================


def ya_disparada(tablero, fila, col):
    return tablero[fila][col] in ("A", "T", "H")


def buscar_barco(barcos, fila, col):
    for barco in barcos:
        for casilla in barco:
            if casilla[0] == fila and casilla[1] == col:
                return barco
    return None


def barco_hundido(tablero, barco):
    for casilla in barco:
        if tablero[casilla[0]][casilla[1]] != "T":
            return False
    return True


def marcar_hundido(tablero, barco):
    for casilla in barco:
        tablero[casilla[0]][casilla[1]] = "H"


def disparo(tablero, barcos, fila, col):

    if ya_disparada(tablero, fila, col):
        return "Repetido"

    if tablero[fila][col] == ".":
        tablero[fila][col] = "A"
        return "Agua"

    # Si no es agua ni repetida, hay un barco sin tocar
    tablero[fila][col] = "T"
    barco = buscar_barco(barcos, fila, col)

    if barco_hundido(tablero, barco):
        marcar_hundido(tablero, barco)
        return "Hundido"

    return "Tocado"




# ============================================================
# FIN DE PARTIDA
# ============================================================
def quedan_barcos(tablero):
    for fila in tablero:
        for casilla in fila:
            if casilla == "B" or casilla == "T":
                return True
    return False



# ============================================================
# PANTALLA Y ENTRADA DE DATOS
# ============================================================
def mostrar_tablero(tablero, ocultar_barcos):
    n = len(tablero)

    linea = "    "
    for i in range(n):
        linea += str(i) + "  "
    print(linea)

    for i in range(n):
        linea = str(i) + "   "
        for casilla in tablero[i]:
            if ocultar_barcos and casilla == "B":
                linea += ".  "
            else:
                linea += casilla + "  "
        print(linea)

    print()


def pedir_numero(mensaje, minimo, maximo):
    valido = False

    while not valido:
        texto = input(mensaje)

        if texto.isdigit():
            numero = int(texto)
            if minimo <= numero <= maximo:
                valido = True
            else:
                print("Debe estar entre", minimo, "y", maximo)
        else:
            print("Introduce un número entero")

    return numero




# ============================================================
# TURNO DEL JUGADOR
# ============================================================
def turno_jugador(tablero_maquina, barcos_maquina):
    n = len(tablero_maquina)

    print("\n----- TU TURNO -----")

    terminado = False
    while not terminado:
        fila = pedir_numero("Fila: ", 0, n - 1)
        columna = pedir_numero("Columna: ", 0, n - 1)

        resultado = disparo(tablero_maquina, barcos_maquina, fila, columna)

        if resultado == "Repetido":
            print("Ya has disparado ahí, elige otra casilla")
        else:
            print("Resultado:", resultado)
            terminado = True




# ============================================================
# JUEGO
# ============================================================
def jugar():
    n = pedir_numero("Tamaño del tablero NxN (mínimo 6): ", TAM_MINIMO, 15)

    tablero_jugador = crear_tablero(n)
    tablero_maquina = crear_tablero(n)

    barcos_jugador = colocar_barcos(tablero_jugador, FLOTA)
    barcos_maquina = colocar_barcos(tablero_maquina, FLOTA)

    objetivos = []
    ganador = ""

    while ganador == "":

        print("\n====================")
        print("TU TABLERO")
        print("====================")
        mostrar_tablero(tablero_jugador, False)

        print("====================")
        print("TABLERO ENEMIGO")
        print("====================")
        mostrar_tablero(tablero_maquina, True)

        turno_jugador(tablero_maquina, barcos_maquina)

        if not quedan_barcos(tablero_maquina):
            ganador = "Jugador"

        if ganador == "":
            print("\n----- TURNO MÁQUINA -----")

            fila, columna, resultado = turno_maquina(tablero_jugador, barcos_jugador, objetivos)

            print("La máquina dispara en:", fila, columna)
            print("Resultado:", resultado)

            if not quedan_barcos(tablero_jugador):
                ganador = "Máquina"

    print()
    mostrar_tablero(tablero_jugador, False)
    mostrar_tablero(tablero_maquina, False)

    if ganador == "Jugador":
        print("¡¡HAS GANADO!!")
    else:
        print("LA MÁQUINA HA GANADO")



# ============================================================
# IA DE LA MÁQUINA
# ============================================================
def anadir_objetivos(tablero, objetivos, fila, columna):
    n = len(tablero)

    if fila + 1 < n and not ya_disparada(tablero, fila + 1, columna):
        objetivos.append([fila + 1, columna])

    if fila - 1 >= 0 and not ya_disparada(tablero, fila - 1, columna):
        objetivos.append([fila - 1, columna])

    if columna + 1 < n and not ya_disparada(tablero, fila, columna + 1):
        objetivos.append([fila, columna + 1])

    if columna - 1 >= 0 and not ya_disparada(tablero, fila, columna - 1):
        objetivos.append([fila, columna - 1])


def turno_maquina(tablero, barcos, objetivos):
    n = len(tablero)

    valida = False
    while not valida:

        if len(objetivos) > 0:
            casilla = objetivos.pop(0)
            fila = casilla[0]
            columna = casilla[1]
        else:
            fila = random.randint(0, n - 1)
            columna = random.randint(0, n - 1)

        if not ya_disparada(tablero, fila, columna):
            valida = True

    resultado = disparo(tablero, barcos, fila, columna)

    if resultado == "Tocado":
        anadir_objetivos(tablero, objetivos, fila, columna)

    if resultado == "Hundido":
        objetivos.clear()

    return fila, columna, resultado



jugar()