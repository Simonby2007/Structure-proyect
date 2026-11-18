class NodoArbol:
    def __init__(self, clave, info):
        self.clave = clave      # lo que se compara (ej. (inversion, ronda))
        self.info = info        # la fila completa del historial
        self.izquierda = None
        self.derecha = None


class ArbolBinarioBusqueda:
    """Árbol binario de búsqueda para ordenar el historial por un criterio.

    Menores a la izquierda, mayores (o iguales) a la derecha.
    Recorrer en orden (izq -> raíz -> der) da la lista ordenada.
    """

    def __init__(self):
        self.raiz = None

    def insertar(self, clave, info):
        nuevo = NodoArbol(clave, info)
        if self.raiz is None:
            self.raiz = nuevo
            return
        actual = self.raiz
        while True:
            if clave < actual.clave:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    return
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    return
                actual = actual.derecha

    def en_orden(self):
        """Devuelve las filas de menor a mayor clave."""
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        if nodo is None:
            return
        self._en_orden(nodo.izquierda, resultado)
        resultado.append(nodo.info)
        self._en_orden(nodo.derecha, resultado)

    def en_orden_inverso(self):
        """Devuelve las filas de mayor a menor clave."""
        resultado = []
        self._en_orden_inverso(self.raiz, resultado)
        return resultado

    def _en_orden_inverso(self, nodo, resultado):
        if nodo is None:
            return
        self._en_orden_inverso(nodo.derecha, resultado)
        resultado.append(nodo.info)
        self._en_orden_inverso(nodo.izquierda, resultado)


# Fila del historial: [ronda, anterior, nuevo, inversion, resultado, saldo]
CRITERIOS = {
    "1": ("Más recientes primero",   lambda f: (f[0], f[0]), True),
    "2": ("Más antiguas primero",    lambda f: (f[0], f[0]), False),
    "3": ("Mayor apuesta primero",   lambda f: (f[3], f[0]), True),
    "4": ("Menor apuesta primero",   lambda f: (f[3], f[0]), False),
    "5": ("Mayor saldo primero",     lambda f: (f[5], f[0]), True),
    "6": ("Menor saldo primero",     lambda f: (f[5], f[0]), False),
}


def ordenar_historial(filas, criterio):
    """Construye un árbol con las filas y las devuelve ordenadas.

    La clave es una tupla (valor, ronda): si dos rondas tienen la misma
    apuesta, la ronda desempata y el orden siempre es estable.
    """
    _, obtener_clave, descendente = CRITERIOS[criterio]
    arbol = ArbolBinarioBusqueda()
    for fila in filas:
        arbol.insertar(obtener_clave(fila), fila)
    return arbol.en_orden_inverso() if descendente else arbol.en_orden()
