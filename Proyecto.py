import random
import matplotlib.pyplot as plt


historial = []
 
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
    """Imprime la matriz historial como tabla."""
    if not historial:
        return
    print("\n===== RESUMEN DE LA PARTIDA =====")
    print(f"{'Ronda':<6}{'Anterior':<10}{'Nuevo':<8}{'Apuesta':<9}{'Resultado':<11}{'Monto':<8}")
    for fila in historial:
        print(f"{fila[0]:<6}{fila[1]:<10}{fila[2]:<8}{fila[3]:<9}{fila[4]:<11}{fila[5]:<8}")
 
    ganadas = sum(1 for fila in historial if fila[4] == "GANO")
    print(f"\nRondas jugadas: {len(historial)}")
    print(f"Rondas ganadas: {ganadas}")
    print(f"Porcentaje de aciertos: {ganadas / len(historial) * 100:.1f}%")
 
 
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
ingreso = ""
 
while ingreso != "enter" and not salir:
    print("")
    print("Ingresar: enter")
    print("Salir: exit")
    ingreso = input("")
 
    if ingreso == "exit":
        salir = True
        print("Gracias por usar el simulador de inversiones")
    elif ingreso != "enter":
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
 
            historial.append([ronda, valor_elegido, valor_elegido2,
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

            
