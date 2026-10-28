# simulador/Cola.py

class ColaLinealEstatica:
    def __init__(self):
        self.MAX = 12
        self.arreglo = [None] * self.MAX
        self.cabeza = -1
        self.cola = -1

    def esta_llena(self) -> bool:
        return self.cola == self.MAX - 1

    def esta_vacia(self) -> bool:
        return self.cabeza == -1 or self.cabeza > self.cola

    def insertar(self, id_transaccion: str) -> bool:
        if self.esta_llena():
            return False

        if self.cabeza == -1:
            self.cabeza = 0

        self.cola += 1
        self.arreglo[self.cola] = id_transaccion
        return True

    def eliminar(self) -> str:
        if self.esta_vacia():
            return None

        transaccion_procesada = self.arreglo[self.frente]
        self.frente += 1
        return transaccion_procesada

    def obtener_representacion(self) -> str:
        if self.esta_vacia():
            return "[ Cola Vacía ]"
        
        texto = ""
        for i in range(self.cabeza, self.cola + 1):
            texto += f"[{self.arreglo[i]}] "
        return texto