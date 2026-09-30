import random
import matplotlib.pyplot as plt


# --- ESTRUCTURA DE DATOS (LISTA DOBLEMENTE ENLAZADA) ---
class Nodo:
    def __init__(self, info):
        self.informacion = info
        self.siguiente = None
        self.anterior = None


class ListaDoblementeEnlazada:
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

    def mostrar(self):
        actual = self.cabeza.siguiente
        if actual == self.cola:
            print("El historial está vacío.")
            return

        print("\n--- HISTORIAL DE APUESTAS ---")
        while actual != self.cola:
            fila = actual.informacion
            print(f"Ronda: {fila[0]} | Ant: {fila[1]} | Nue: {fila[2]} | Apuesta: {fila[3]} | Res: {fila[4]} | Saldo: {fila[5]}")
            actual = actual.siguiente

    def mostrar_regreso(self):
        actual = self.cola.anterior
        if actual == self.cabeza:
            print("El historial está vacío.")
            return

        print("\n--- HISTORIAL INVERTIDO ---")
        while actual != self.cabeza:
            fila = actual.informacion
            print(f"Ronda: {fila[0]} | Ant: {fila[1]} | Nue: {fila[2]} | Apuesta: {fila[3]} | Res: {fila[4]} | Saldo: {fila[5]}")
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


historial = ListaDoblementeEnlazada()

# Arreglo con los números generados (eje Y de la gráfica)
numeros = []

ronda = 0


# Funciones
def pedir_entero(mensaje):
    """Pide un entero positivo y repite hasta que sea válido."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            print("Error: Ingrese un número mayor que 0")
        except ValueError:
            print("Error: Ingrese un número entero")


def pedir_apuesta(monto, mensaje):
    """Pide una apuesta que no supere el monto disponible."""
    apuesta = pedir_entero(mensaje)
    while apuesta > monto:
        print("Error: Ingrese un valor menor o igual al monto total")
        apuesta = pedir_entero("Apuesta: ")
    return apuesta


def actualizar_grafica(color):
    """Agrega el último número a la gráfica y la redibuja."""
    x = len(numeros) - 1
    linea.set_data(range(len(numeros)), numeros)
    ax.scatter(x, numeros[-1], color=color, zorder=3)
    ax.set_xlim(-0.5, max(10, len(numeros)))
    plt.pause(0.1)


def mostrar_resumen():
    """Imprime el historial recorriendo la lista enlazada."""
    actual = historial.cabeza.siguiente
    if actual == historial.cola:
        return

    print("\n===== RESUMEN DE LA PARTIDA =====")
    total = 0
    ganadas = 0

    while actual != historial.cola:
        fila = actual.informacion
        print(f"Ronda: {fila[0]:<4} | Ant: {fila[1]:<3} | Nue: {fila[2]:<3} | Apuesta: {fila[3]:<5} | Res: {fila[4]:<7} | Saldo: {fila[5]}")
        total += 1
        if fila[4] == "GANO":
            ganadas += 1
        actual = actual.siguiente

    print(f"\nRondas jugadas: {total}")
    print(f"Rondas ganadas: {ganadas}")
    if total > 0:
        print(f"Porcentaje de aciertos: {(ganadas / total) * 100:.1f}%")


# Registro de usuario
nombre = input("Ingrese nombre: ")
contraseña = input("Ingrese contraseña: ")
confirmar = input("Confirme contraseña: ")

while confirmar != contraseña:
    print("Error: Las contraseñas no coinciden")
    confirmar = input("Ingrese de nuevo la contraseña: ")

monto = 1000
print("Bienvenido " + nombre + " al simulador de inversiones")
print("Monto actual --> " + str(monto) + "$")

# Menú 
salir = False
ingreso = "espera"

while ingreso != "" and not salir:
    print("")
    print("Presione ENTER para jugar")
    print("Salir: exit")
    ingreso = input("")

    if ingreso == "exit":
        salir = True
        print("Gracias por usar el simulador de inversiones")
    elif ingreso != "":
        print("Error: Ingrese un valor valido")


# Simulador
if not salir:
    # Ventana de la gráfica (se crea una sola vez)
    plt.ion()
    fig, ax = plt.subplots()
    linea, = ax.plot([], [], color="gray", linewidth=1)
    ax.set_xlabel("Ronda")
    ax.set_ylabel("Número generado")
    ax.set_ylim(0, 101)
    ax.set_title("Historial de números")

    # Primer número y primera apuesta
    valor_elegido = random.randint(1, 100)
    print("\nPRIMER VALOR: " + str(valor_elegido))
    numeros.append(valor_elegido)
    actualizar_grafica("blue")

    monto_temporal = pedir_apuesta(monto, "¿Cuánto desea apostar?: ")

    while not salir:
        print("\nMonto actual: " + str(monto) + "$ | Apuesta: " + str(monto_temporal) + "$")
        print("El siguiente número será: ")
        print("MAYOR: 1")
        print("MENOR: 2")
        print("Cambiar apuesta: 3")
        print("Ver menú historial: 4")
        print("Salir: exit")

        comparacion = input()

        if comparacion in ("1", "2"):
            valor_elegido2 = random.randint(1, 100)
            print("NUEVO VALOR: " + str(valor_elegido2))
            ronda += 1
            numeros.append(valor_elegido2)

            if valor_elegido2 == valor_elegido:
                resultado = "EMPATE"
                color = "orange"
                print("Empate! No ganas ni pierdes. Monto actual -> " + str(monto) + "$")
            else:
                if comparacion == "1":
                    acerto = valor_elegido2 > valor_elegido
                else:
                    acerto = valor_elegido2 < valor_elegido

                if acerto:
                    monto += monto_temporal
                    resultado = "GANO"
                    color = "green"
                    print("Ganaste! Monto actual -> " + str(monto) + "$")
                else:
                    monto -= monto_temporal
                    resultado = "PERDIO"
                    color = "red"
                    print("Perdiste! Monto actual -> " + str(monto) + "$")

            historial.insertar([ronda, valor_elegido, valor_elegido2,
                              monto_temporal, resultado, monto])
            actualizar_grafica(color)
            valor_elegido = valor_elegido2

            if monto <= 0:
                print("No tienes dinero para seguir jugando")
                salir = True
            elif monto < monto_temporal:
                print("Tu monto es menor a tu apuesta, ingresa una nueva")
                monto_temporal = pedir_apuesta(monto, "Nueva apuesta: ")

        elif comparacion == "3":
            monto_temporal = pedir_apuesta(monto, "Ingrese nuevo valor para apostar: ")

        elif comparacion == "4":
            opc_hist = ""
            while opc_hist != "4":
                print("\n--- MENÚ HISTORIAL ---")
                print("1. Ver historial completo")
                print("2. Ver historial al revés")
                print("3. Eliminar una ronda por número")
                print("4. Volver al juego")
                opc_hist = input("Elija una opción: ")

                if opc_hist == "1":
                    historial.mostrar()
                elif opc_hist == "2":
                    historial.mostrar_regreso()
                elif opc_hist == "3":
                    num = int(input("Ingrese el número de ronda a eliminar: "))
                    historial.eliminar(num)
                elif opc_hist == "4":
                    print("Volviendo al juego...")
                else:
                    print("Error: Opción inválida")

        elif comparacion == "exit":
            salir = True
            print("Gracias por usar el simulador de inversiones")

        else:
            print("Error: Ingrese un valor valido")

    # Final
    mostrar_resumen()
    print("Cierra la ventana de la gráfica para terminar.")
    plt.ioff()
    plt.show()