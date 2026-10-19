def crear_tablero(N):
    tablero = []
    for _ in range(N):
        fila = []
        for _ in range(N):
            fila.append(".")
        tablero.append(fila)
    return tablero


def mostrar_tablero(tablero, ocultar_barcos=True):
    N = len(tablero)

    linea = "   "
    for i in range(N):
        linea += str(i+1) + " "
    print(linea)

    for i in range(N):
        fila = str(i+1) + "  "
        for c in tablero[i]:
            if ocultar_barcos and c in ("B", "T", "H"):
                fila += ". "
            else:
                fila += c + " "
        print(fila)
    print()


def puede_colocar(tablero, x, y, tamaño, horizontal):
    N = len(tablero)

    if horizontal:
        if y + tamaño > N:
            return False
        for i in range(tamaño):
            if tablero[x][y+i] != ".":
                return False
        return True
    else:
        if x + tamaño > N:
            return False
        for i in range(tamaño):
            if tablero[x+i][y] != ".":
                return False
        return True


def colocar_barco(tablero, x, y, tamaño, horizontal):
    if horizontal:
        for i in range(tamaño):
            tablero[x][y+i] = "B"
    else:
        for i in range(tamaño):
            tablero[x+i][y] = "C"


def colocar_barcos(tablero, lista_barcos):
    import random
    N = len(tablero)

    for tamaño in lista_barcos:
        colocado = False
        while not colocado:
            x = random.randint(0, N-1)
            y = random.randint(0, N-1)

            horizontal = True
            if random.randint(0, 1) == 1:
                horizontal = False

            if puede_colocar(tablero, x, y, tamaño, horizontal):
                colocar_barco(tablero, x, y, tamaño, horizontal)
                colocado = True




print("1) Creando tablero...")
tablero = crear_tablero(8)
mostrar_tablero(tablero, ocultar_barcos=False)

print("2) Colocando barcos...")
barcos = [1, 1, 2, 2, 3, 4]
colocar_barcos(tablero, barcos)
mostrar_tablero(tablero, ocultar_barcos=False)

print("3) Probando puede_colocar en (0,0) tamaño 3 horizontal...")
print(puede_colocar(tablero, 0, 0, 3, True))

print("4) Colocando barco manual en (0,0) tamaño 3 horizontal...")
if puede_colocar(tablero, 0, 0, 3, True):
    colocar_barco(tablero, 0, 0, 3, True)

mostrar_tablero(tablero, ocultar_barcos=False)