import matplotlib.pyplot as plt


class Grafica:
    """Ventana con el historial de números generados (eje Y)."""

    def __init__(self):
        self.numeros = []
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.linea, = self.ax.plot([], [], color="gray", linewidth=1)
        self.ax.set_xlabel("Ronda")
        self.ax.set_ylabel("Número generado")
        self.ax.set_ylim(0, 101)
        self.ax.set_title("Historial de números")

    def agregar(self, numero, color):
        """Agrega un número a la gráfica y la redibuja."""
        self.numeros.append(numero)
        x = len(self.numeros) - 1
        self.linea.set_data(range(len(self.numeros)), self.numeros)
        self.ax.scatter(x, numero, color=color, zorder=3)
        self.ax.set_xlim(-0.5, max(10, len(self.numeros)))
        plt.pause(0.1)

    def refrescar(self):
        """Mantiene la ventana viva durante una espera, sin robar el foco."""
        self.fig.canvas.flush_events()

    def mostrar_final(self):
        plt.ioff()
        plt.show()
