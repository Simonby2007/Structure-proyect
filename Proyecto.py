import random
salir = False
ingreso = ""
while salir == False:
    nombre = input("Ingrese nombre: ")
    contraseña = input("Ingrese contraseña: ")
    confirmar = input("Confirme contraseña: ")
    while confirmar != contraseña:
        print("Error: Contraseña incorrecta")
        confirmar = input("Ingrese de nuevo la contraseña")
    monto = 1000
    print("Bienvenido " + nombre + " al simulador de inversiones")
    print("Monto actual --> " + str(monto) + "$")
    while salir == False and ingreso != "enter":
        print("")
        print("Ingresar: enter")
        print("Salir: exit")
        ingreso = input("")
        if ingreso == "exit":
            salir = True
            print("Gracias por usar el simulador de inversiones")
        elif ingreso == "enter":
            pass
        else:
            print("Error: Ingrese un valor valido")
        while salir == False:
            valor_elegido = random.randint(1, 100)
            print("PRIMER VALOR: " + str(valor_elegido))
            monto_temporal = int(input("¿Cuánto desea ingresar?: "))
            while monto_temporal > monto:
                print("Error: Ingrse un valor menor o igual al monto total")
                monto_temporal = int(input())
            monto = monto - monto_temporal
            while salir == False:
                valor_elegido2 = random.randint(1, 100)
                print("El siguiente número será: ")
                print("MAYOR: 1.)")
                print("MENOR: 2.)")
                print("Ingrese nuevo valor para apostar: 3.)")
                print("salir: exit")
                comparacion = input()
                match comparacion:
                    case '1':
                        print("SEGUNDO VALOR: " + str(valor_elegido2))
                        if valor_elegido2 > valor_elegido:
                            monto = monto + monto_temporal
                            print("Ganaste! Monto actual -> " + str(monto) + "$")
                            valor_elegido = valor_elegido2
                        else:
                            print("Perdiste! Monto actual -> " + str(monto) + "$")
                            if monto == 0:
                                print("No tienes dinero para seguir jugando")
                                salir = True
                        valor_elegido = valor_elegido2
                    case '2':
                        print("SEGUNDO VALOR: " + str(valor_elegido2))
                        if valor_elegido2 < valor_elegido:
                            monto = monto + monto_temporal
                            print("Ganaste! Monto actual -> " + str(monto) + "$")
                            valor_elegido = valor_elegido2
                        else:
                            print("Perdiste! Monto actual -> " + str(monto) + "$")
                            if monto == 0:
                                print("No tienes dinero para seguir jugando")
                                salir = True
                        valor_elegido = valor_elegido2
                    case '3':
                        monto = monto + monto_temporal
                        monto_temporal = int(input("Ingrese nuevo valor para apostar: "))
                        while monto_temporal > monto:
                            print("Error: Ingrese un valor menor o igual al monto total")
                            monto_temporal = int(input())
                    case 'exit':
                        salir = True
                        print("Gracias por usar el simulador de inversiones")
                    case _:
                        print("Error: Ingrese un valor valido")


            
            
