# Structure-proyects
lo hice en py
import random

salir = False
ingreso = ""

while not salir:
    # INGRESO DEL USUARIO
    monto = 1000

    print("Ingrese nombre:")
    nombre = input()

    print("Ingrese contraseña:")
    contraseña = input()

    print("Confirme contraseña:")
    confirmar = input()

    while contraseña != confirmar:
        print("Error: Contraseña incorrecta")
        confirmar = input()

    # INTERFAZ DE ENTRADA
    print(f"Bienvenido {nombre} al simulador de inversiones")
    print(f"Monto actual -> {monto}$")

    while not salir and ingreso != "enter":
        print()
        print("Ingresar: enter")
        print("Salir: exit")

        ingreso = input()

        if ingreso == "exit":
            salir = True
            print("Gracias por usar el simulador de inversiones")

        elif ingreso == "enter":
            pass

        else:
            print("Error: Ingrese un valor valido")

    # JUEGO
    while not salir:

        # CREACIÓN DEL VECTOR GENERADOR DE NÚMEROS ALEATORIOS
        numeros_apuesta = list(range(1, 101))

        valor_elegido = random.choice(numeros_apuesta)

        print(f"PRIMER VALOR: {valor_elegido}")

        print("¿Cuánto desea ingresar?")
        monto_temp = int(input())

        while monto_temp > monto:
            print("Error: Ingrese un valor menor o igual al monto total")
            monto_temp = int(input())

        monto = monto - monto_temp

        # EMPEZAR ALGORITMO DE COMPARACIÓN
        while not salir:

            valor_elegido_2 = random.choice(numeros_apuesta)

            print("¿El siguiente numero será:")
            print("MAYOR: 1.)")
            print("MENOR: 2.)")
            print("Ingresar nuevo valor para apostar: 3.)")
            print("salir: exit")

            comparacion = input()

            if comparacion == "1":

                valor_elegido_2 = random.choice(numeros_apuesta)

                print(f"SEGUNDO VALOR: {valor_elegido_2}")

                if valor_elegido_2 > valor_elegido:
                    monto = monto + monto_temp
                    print(f"Ganaste! Monto actual -> {monto}$")
                else:
                    print(f"Perdiste! Monto actual -> {monto}$")

                    if monto == 0:
                        print("No tienes dinero para seguir jugando")
                        salir = True

                valor_elegido = valor_elegido_2

            elif comparacion == "2":

                valor_elegido_2 = random.choice(numeros_apuesta)

                print(f"SEGUNDO VALOR: {valor_elegido_2}")

                if valor_elegido_2 < valor_elegido:
                    monto_temp = monto_temp * 2
                    monto = monto + monto_temp
                    print(f"Ganaste! Monto actual -> {monto}$")
                else:
                    print(f"Perdiste! Monto actual -> {monto}$")

                    if monto == 0:
                        print("No tienes dinero para seguir jugando")
                        salir = True

                valor_elegido = valor_elegido_2

            elif comparacion == "3":

                monto = monto + monto_temp

                print("Ingrese nuevo valor para apostar:")
                monto_temp = int(input())

                while monto_temp > monto:
                    print("Error: Ingrese un valor menor o igual al monto total")
                    monto_temp = int(input())

                monto = monto - monto_temp

            elif comparacion == "exit":

                salir = True
                print("Gracias por usar el simulador de inversiones")

            else:
                print("Error: Ingrese un valor valido")
