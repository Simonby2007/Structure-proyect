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


def pedir_inversion(monto, mensaje):
    """Pide una inversión que no supere el monto disponible."""
    inversion = pedir_entero(mensaje)
    while inversion > monto:
        print("Error: Ingrese un valor menor o igual al monto total")
        inversion = pedir_entero(mensaje)
    return inversion
