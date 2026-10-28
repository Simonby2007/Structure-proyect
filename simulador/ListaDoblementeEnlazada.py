class Nodo:
    def __init__(self, info):
        self.informacion = info
        self.siguiente = None
        self.anterior = None


class ListaDoblementeEnlazada:
    """Historial de rondas con nodos centinela (cabeza y cola vacías).

    Cada fila es: [ronda, valor_anterior, valor_nuevo, inversion, resultado, saldo]
    """

    def __init__(self):
        self.cabeza = Nodo(None)
        self.cola = Nodo(None)
        self.cabeza.siguiente = self.cola
        self.cola.anterior = self.cabeza

    def insertar(self, info):
        nuevo_nodo = Nodo(info)
        ultimo_nodo = self.cola.anterior
        nuevo_nodo.anterior = ultimo_nodo
        nuevo_nodo.siguiente = self.cola
        ultimo_nodo.siguiente = nuevo_nodo
        self.cola.anterior = nuevo_nodo

    @staticmethod
    def _linea(fila):
        return (f"Ronda: {fila[0]} | Ant: {fila[1]} | Nue: {fila[2]} | "
                f"Invertido: {fila[3]} | Res: {fila[4]} | Saldo: {fila[5]}")

    def mostrar(self):
        actual = self.cabeza.siguiente
        if actual == self.cola:
            print("El historial está vacío.")
            return

        print("\n--- HISTORIAL DE INVERSIÓN ---")
        while actual != self.cola:
            print(self._linea(actual.informacion))
            actual = actual.siguiente

    def mostrar_regreso(self):
        actual = self.cola.anterior
        if actual == self.cabeza:
            print("El historial está vacío.")
            return

        print("\n--- HISTORIAL INVERTIDO ---")
        while actual != self.cabeza:
            print(self._linea(actual.informacion))
            actual = actual.anterior

    def eliminar(self, num_ronda):
        actual = self.cabeza.siguiente
        while actual != self.cola:
            if actual.informacion[0] == num_ronda:
                anterior = actual.anterior
                siguiente = actual.siguiente
                anterior.siguiente = siguiente
                siguiente.anterior = anterior
                print("Ronda eliminada con éxito.")
                return
            actual = actual.siguiente
        print("No se encontró esa ronda.")

    def mostrar_resumen(self):
        """Imprime el resumen final recorriendo la lista."""
        actual = self.cabeza.siguiente
        if actual == self.cola:
            return

        print("\n===== RESUMEN DE LA PARTIDA =====")
        total = 0
        ganadas = 0

        while actual != self.cola:
            fila = actual.informacion
            print(f"Ronda: {fila[0]:<4} | Ant: {fila[1]:<3} | Nue: {fila[2]:<3} | "
                  f"Inversión: {fila[3]:<5} | Res: {fila[4]:<7} | Saldo: {fila[5]}")
            total += 1
            if fila[4] == "GANO":
                ganadas += 1
            actual = actual.siguiente

        print(f"\nRondas jugadas: {total}")
        print(f"Rondas ganadas: {ganadas}")
        print(f"Porcentaje de aciertos: {(ganadas / total) * 100:.1f}%")
