import math
import random

import Teclado
from Entradas import pedir_entero, pedir_inversion
from Grafica import Grafica
from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from Pila import Pila

ESPERA_DESHACER = 3  # segundos para poder deshacer pulsando ESC


class Partida:
    def __init__(self, monto_inicial=1000):
        self.monto = monto_inicial
        self.monto_temporal = 0     # lo que se invierte en cada ronda
        self.valor_actual = 0       # número mostrado en consola
        self.ronda = 0
        self.historial = ListaDoblementeEnlazada()
        self.deshacer = Pila()      # estados anteriores a cada jugada
        self.grafica = None

    # ---------- Bucle principal ----------
    def jugar(self):
        self.grafica = Grafica()
        self.valor_actual = random.randint(1, 100)
        print("\nPRIMER VALOR: " + str(self.valor_actual))
        self.grafica.agregar(self.valor_actual, "blue")
        self.monto_temporal = pedir_inversion(self.monto, "¿Cuánto desea invertir?: ")

        seguir = True
        while seguir:
            self._mostrar_menu()
            opcion = input()

            if opcion in ("1", "2"):
                seguir = self._jugar_ronda(opcion)
            elif opcion == "3":
                self.monto_temporal = pedir_inversion(
                    self.monto, "Ingrese nuevo valor para invertir: ")
            elif opcion == "4":
                self._menu_historial()
            elif opcion == "exit":
                print("Gracias por usar el simulador de inversiones")
                seguir = False
            else:
                print("Error: Ingrese un valor valido")

        self.historial.mostrar_resumen()
        print("Cierra la ventana de la gráfica para terminar.")
        self.grafica.mostrar_final()

    def _mostrar_menu(self):
        print("\nMonto actual: " + str(self.monto) + "$ | Monto invertido: "
              + str(self.monto_temporal) + "$")
        print("El siguiente número será: ")
        print("MAYOR: 1")
        print("MENOR: 2")
        print("Cambiar monto invertido: 3")
        print("Ver menú historial: 4")
        print("Salir: exit")
        print(f"(Al elegir 1 o 2 tienes {ESPERA_DESHACER} s para deshacer con ESC)")

    # ---------- Una ronda, con opción de deshacer ----------
    def _jugar_ronda(self, opcion):
        """Devuelve False si el jugador se quedó sin dinero."""
        # Se guarda el estado ANTES de la jugada: es lo que se restaura con ESC.
        self.deshacer.push({
            "monto": self.monto,
            "monto_temporal": self.monto_temporal,
            "valor_actual": self.valor_actual,
            "ronda": self.ronda,
        })

        if self._esperar_deshacer():
            self._restaurar(self.deshacer.pop())
            print("Jugada deshecha. Elige de nuevo.")
            return True

        self.deshacer.vaciar()  # pasó el tiempo: la jugada ya es definitiva
        return self._resolver(opcion)

    def _esperar_deshacer(self):
        """Cuenta regresiva. Devuelve True si el jugador pulsó ESC."""
        ultimo = None

        def tick(restante):
            nonlocal ultimo
            segundo = math.ceil(restante)
            if segundo != ultimo:
                ultimo = segundo
                print(f"\r  Revelando en {segundo}... (ESC para deshacer) ",
                      end="", flush=True)
            self.grafica.refrescar()

        print()
        deshecho = Teclado.esperar_esc(ESPERA_DESHACER, tick)
        print("\r" + " " * 50 + "\r", end="", flush=True)  # borra la cuenta regresiva
        return deshecho

    def _restaurar(self, estado):
        self.monto = estado["monto"]
        self.monto_temporal = estado["monto_temporal"]
        self.valor_actual = estado["valor_actual"]
        self.ronda = estado["ronda"]

    def _resolver(self, opcion):
        """Genera el número nuevo, compara y actualiza el monto."""
        nuevo = random.randint(1, 100)
        print("NUEVO VALOR: " + str(nuevo))
        self.ronda += 1

        if nuevo == self.valor_actual:
            resultado = "EMPATE"
            color = "orange"
            print("Empate! No ganas ni pierdes. Monto actual -> " + str(self.monto) + "$")
        else:
            if opcion == "1":
                acerto = nuevo > self.valor_actual
            else:
                acerto = nuevo < self.valor_actual

            if acerto:
                self.monto += self.monto_temporal
                resultado = "GANO"
                color = "green"
                print("Ganaste! Monto actual -> " + str(self.monto) + "$")
            else:
                self.monto -= self.monto_temporal
                resultado = "PERDIO"
                color = "red"
                print("Perdiste! Monto actual -> " + str(self.monto) + "$")

        self.historial.insertar([self.ronda, self.valor_actual, nuevo,
                                 self.monto_temporal, resultado, self.monto])
        self.grafica.agregar(nuevo, color)
        self.valor_actual = nuevo

        if self.monto <= 0:
            print("No tienes dinero para seguir jugando")
            return False
        if self.monto < self.monto_temporal:
            print("Tu monto total es menor a tu monto elegido, ingresa una nueva")
            self.monto_temporal = pedir_inversion(self.monto, "Nueva apuesta: ")
        return True

    # ---------- Menú del historial ----------
    def _menu_historial(self):
        opcion = ""
        while opcion != "4":
            print("\n--- MENÚ HISTORIAL ---")
            print("1. Ver historial completo")
            print("2. Ver historial al revés")
            print("3. Eliminar una ronda por número")
            print("4. Volver al juego")
            opcion = input("Elija una opción: ")

            if opcion == "1":
                self.historial.mostrar()
            elif opcion == "2":
                self.historial.mostrar_regreso()
            elif opcion == "3":
                num = pedir_entero("Ingrese el número de ronda a eliminar: ")
                self.historial.eliminar(num)
            elif opcion == "4":
                print("Volviendo al juego...")
            else:
                print("Error: Opción inválida")
