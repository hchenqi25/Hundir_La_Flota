# ============================================================
# ---------------------- TABLERO ------------------------------
# ============================================================

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
        linea += str(i) + " "
    print(linea)

    for i in range(N):
        fila = str(i) + "  "
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
            tablero[x+i][y] = "B"


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


# ============================================================
# ---------------------- LÓGICA DEL DISPARO -------------------
# ============================================================

def disparo(tablero, x, y):
    casilla = tablero[x][y]

    if casilla == ".":
        tablero[x][y] = "A"
        return "Agua"

    if casilla == "B":
        tablero[x][y] = "T"

        if barco_hundido(tablero, x, y):
            marcar_hundido(tablero, x, y)
            return "Hundido"

        return "Tocado"

    return "Ya disparado"


def barco_hundido(tablero, x, y):
    N = len(tablero)
    pila = [(x, y)]
    visitadas = []

    while len(pila) > 0:
        cx, cy = pila.pop()

        repetida = False
        for vx, vy in visitadas:
            if vx == cx and vy == cy:
                repetida = True

        if repetida == False:
            visitadas.append((cx, cy))

            if tablero[cx][cy] == "B":
                return False

            if cx+1 < N and tablero[cx+1][cy] in ("B", "T"):
                pila.append((cx+1, cy))
            if cx-1 >= 0 and tablero[cx-1][cy] in ("B", "T"):
                pila.append((cx-1, cy))
            if cy+1 < N and tablero[cx][cy+1] in ("B", "T"):
                pila.append((cx, cy+1))
            if cy-1 >= 0 and tablero[cx][cy-1] in ("B", "T"):
                pila.append((cx, cy-1))

    return True


def marcar_hundido(tablero, x, y):
    N = len(tablero)
    pila = [(x, y)]
    visitadas = []

    while len(pila) > 0:
        cx, cy = pila.pop()

        repetida = False
        for vx, vy in visitadas:
            if vx == cx and vy == cy:
                repetida = True

        if repetida == False:
            visitadas.append((cx, cy))

            if tablero[cx][cy] == "T":
                tablero[cx][cy] = "H"

            if cx+1 < N and tablero[cx+1][cy] in ("B", "T"):
                pila.append((cx+1, cy))
            if cx-1 >= 0 and tablero[cx-1][cy] in ("B", "T"):
                pila.append((cx-1, cy))
            if cy+1 < N and tablero[cx][cy+1] in ("B", "T"):
                pila.append((cx, cy+1))
            if cy-1 >= 0 and tablero[cx][cy-1] in ("B", "T"):
                pila.append((cx, cy-1))



tablero = crear_tablero(8)
print("TABLERO VACÍO:")
mostrar_tablero(tablero, False)

colocar_barcos(tablero, [1,1,2,2,3,4])
print("TABLERO CON BARCOS:")
mostrar_tablero(tablero, False)

print("DISPARO EN (0,0):", disparo(tablero, 0, 0))
mostrar_tablero(tablero, False)

print("DISPARO EN (3,3):", disparo(tablero, 3, 3))
mostrar_tablero(tablero, False)
