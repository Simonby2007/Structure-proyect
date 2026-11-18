from Partida import Partida

MONTO_INICIAL = 1000


def registrar_usuario():
    nombre = input("Ingrese nombre: ")
    contraseña = input("Ingrese contraseña: ")
    confirmar = input("Confirme contraseña: ")

    while confirmar != contraseña:
        print("Error: Las contraseñas no coinciden")
        confirmar = input("Ingrese de nuevo la contraseña: ")
    return nombre


def menu_inicial():
    """Devuelve True si el usuario quiere jugar y False si quiere salir."""
    while True:
        print("")
        print("Presione ENTER para jugar")
        print("Salir: exit")
        ingreso = input("")

        if ingreso == "":
            return True
        if ingreso == "exit":
            print("Gracias por usar el simulador de inversiones")
            return False
        print("Error: Ingrese un valor valido")


def main():
    nombre = registrar_usuario()
    print("Bienvenido " + nombre + " al simulador de inversiones")
    print("Monto actual --> " + str(MONTO_INICIAL) + "$")

    if menu_inicial():
        Partida(MONTO_INICIAL).jugar()


if __name__ == "__main__":
    main()
