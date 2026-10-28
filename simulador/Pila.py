class Pila:
    """Pila (LIFO) con lista simplemente enlazada.

    El tope es `cabeza`, así que push, pop y peek son O(1).
    """

    class Nodo:
        def __init__(self, info, siguiente=None):
            self.info = info
            self.siguiente = siguiente

    def __init__(self):
        self.cabeza = None  # tope de la pila

    def push(self, objeto):
        self.cabeza = self.Nodo(objeto, self.cabeza)

    def pop(self):
        """Saca y devuelve el tope. Devuelve None si la pila está vacía."""
        if self.cabeza is None:
            return None
        informacion = self.cabeza.info
        self.cabeza = self.cabeza.siguiente
        return informacion

    def peek(self):
        """Devuelve el tope sin sacarlo (None si está vacía)."""
        return None if self.cabeza is None else self.cabeza.info

    def vacia(self):
        return self.cabeza is None

    def vaciar(self):
        self.cabeza = None

    def mostrar(self):
        """Imprime del tope hacia el fondo."""
        actual = self.cabeza
        while actual is not None:
            print(actual.info)
            actual = actual.siguiente
