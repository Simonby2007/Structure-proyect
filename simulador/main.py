# simulador/main.py

import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from Cola import ColaLinealEstatica


class SimuladorInversionesApp:
    def __init__(self, root, nombre_usuario, monto_inicial):
        self.root = root
        self.nombre_usuario = nombre_usuario
        self.monto = monto_inicial
        
        self.root.title(f"Simulador Pro | Usuario: {self.nombre_usuario}")
        self.root.geometry("1000x730")
        self.root.config(bg="#1e1e2e")

        # --- DANDO PRIORIDAD A LA LISTA DOBLEMENTE ENLAZADA ---
        self.historial = ListaDoblementeEnlazada()
        
        # Cola estática opcional para transacciones
        self.cola_transacciones = ColaLinealEstatica()
        self.contador_tx = 101

        self.numeros = []
        self.ronda = 0
        self.monto_temporal = 100
        self.valor_elegido = random.randint(1, 100)
        self.numeros.append(self.valor_elegido)

        self.crear_interfaz()

    def crear_interfaz(self):
        # Encabezado
        header_frame = tk.Frame(self.root, bg="#252538", pady=12)
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame, text=f"📈 SIMULADOR DE INVERSIONES (Historial en Lista Doblemente Enlazada)", 
            font=("Segoe UI", 13, "bold"), fg="#cdd6f4", bg="#252538"
        ).pack()

        # Tarjetas Superiores
        info_frame = tk.Frame(self.root, bg="#1e1e2e", pady=8)
        info_frame.pack(fill=tk.X, padx=15)

        card_monto = tk.Frame(info_frame, bg="#313244", padx=15, pady=8)
        card_monto.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(card_monto, text="MONTO DISPONIBLE", font=("Segoe UI", 8), fg="#a6adc8", bg="#313244").pack(anchor="w")
        self.lbl_monto = tk.Label(card_monto, text=f"${self.monto}", font=("Segoe UI", 13, "bold"), fg="#a6e3a1", bg="#313244")
        self.lbl_monto.pack(anchor="w")

        card_inv = tk.Frame(info_frame, bg="#313244", padx=15, pady=8)
        card_inv.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(card_inv, text="APUESTA ACTUAL", font=("Segoe UI", 8), fg="#a6adc8", bg="#313244").pack(anchor="w")
        self.lbl_apuesta = tk.Label(card_inv, text=f"${self.monto_temporal}", font=("Segoe UI", 13, "bold"), fg="#89b4fa", bg="#313244")
        self.lbl_apuesta.pack(anchor="w")

        card_val = tk.Frame(info_frame, bg="#313244", padx=15, pady=8)
        card_val.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(card_val, text="VALOR REFERENCIA", font=("Segoe UI", 8), fg="#a6adc8", bg="#313244").pack(anchor="w")
        self.lbl_valor_actual = tk.Label(card_val, text=str(self.valor_elegido), font=("Segoe UI", 13, "bold"), fg="#fab387", bg="#313244")
        self.lbl_valor_actual.pack(anchor="w")

        # Cuerpo Principal
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Panel Izquierdo (Controles y Historial Directo)
        left_panel = tk.Frame(main_frame, bg="#252538", padx=15, pady=12)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        tk.Label(left_panel, text="¿El próximo número será?", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#252538").pack(anchor="w", pady=(0, 8))

        btn_mayor = tk.Button(left_panel, text="📈 MAYOR", font=("Segoe UI", 10, "bold"), bg="#a6e3a1", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=22, pady=6, command=lambda: self.jugar("1"))
        btn_mayor.pack(pady=5)

        btn_menor = tk.Button(left_panel, text="📉 MENOR", font=("Segoe UI", 10, "bold"), bg="#f38ba8", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=22, pady=6, command=lambda: self.jugar("2"))
        btn_menor.pack(pady=5)

        tk.Frame(left_panel, height=2, bg="#313244", bd=0).pack(fill=tk.X, pady=10)

        btn_cambiar = tk.Button(left_panel, text="💵 Cambiar Apuesta", font=("Segoe UI", 9), bg="#89b4fa", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=22, pady=5, command=self.cambiar_apuesta)
        btn_cambiar.pack(pady=3)

        # BOTÓN PRINCIPAL PARA VER EL HISTORIAL DE LA LISTA DOBLEMENTE ENLAZADA
        btn_historial = tk.Button(left_panel, text="📜 Ver Historial (Lista Enlazada)", font=("Segoe UI", 9, "bold"), bg="#cba6f7", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=22, pady=6, command=self.mostrar_ventana_historial)
        btn_historial.pack(pady=3)

        btn_salir = tk.Button(left_panel, text="❌ Salir", font=("Segoe UI", 9), bg="#45475a", fg="#cdd6f4", relief=tk.FLAT, cursor="hand2", width=22, pady=5, command=self.root.quit)
        btn_salir.pack(pady=(12, 0))

        # Consola de eventos en pantalla
        tk.Label(left_panel, text="Registro de jugadas:", font=("Segoe UI", 8, "bold"), fg="#a6adc8", bg="#252538").pack(anchor="w", pady=(10, 2))
        self.txt_logs = tk.Text(left_panel, height=8, width=28, font=("Consolas", 8), bg="#181825", fg="#cdd6f4", bd=0, padx=5, pady=5)
        self.txt_logs.pack(fill=tk.BOTH, expand=True)
        self.txt_logs.insert(tk.END, f">> Sesión iniciada. Referencia: {self.valor_elegido}\n")

        # Panel Derecho (Gráfica)
        right_panel = tk.Frame(main_frame, bg="#252538", bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.fig.patch.set_facecolor('#252538')
        self.ax.set_facecolor('#181825')
        
        self.linea, = self.ax.plot([], [], color="#89b4fa", linewidth=1.5)
        self.ax.set_xlabel("Ronda", fontsize=9, color="#cdd6f4")
        self.ax.set_ylabel("Valor", fontsize=9, color="#cdd6f4")
        self.ax.set_ylim(0, 101)
        self.ax.set_title("Evolución de Tendencia", fontsize=10, color="#cdd6f4", pad=10)
        self.ax.tick_params(colors="#a6adc8", labelsize=8)
        self.ax.grid(True, linestyle="--", alpha=0.15)

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.actualizar_grafica("#89b4fa")

    def actualizar_grafica(self, color):
        x = len(self.numeros) - 1
        self.linea.set_data(range(len(self.numeros)), self.numeros)
        self.ax.scatter(x, self.numeros[-1], color=color, zorder=3, s=35)
        self.ax.set_xlim(-0.5, max(10, len(self.numeros)))
        self.canvas.draw()

    def jugar(self, comparacion):
        if self.monto <= 0:
            messagebox.showwarning("Game Over", "Sin fondos.")
            return

        valor_elegido2 = random.randint(1, 100)
        self.ronda += 1
        self.numeros.append(valor_elegido2)
        resultado = ""
        color = "#89b4fa"

        if valor_elegido2 == self.valor_elegido:
            resultado = "EMPATE"
            color = "#fab387"
            mensaje = f"Ronda {self.ronda}: Empate ({valor_elegido2})."
        else:
            acerto = (comparacion == "1" and valor_elegido2 > self.valor_elegido) or \
                     (comparacion == "2" and valor_elegido2 < self.valor_elegido)
            if acerto:
                self.monto += self.monto_temporal
                resultado = "GANO"
                color = "#a6e3a1"
                mensaje = f"Ronda {self.ronda}: ¡Ganó! (+${self.monto_temporal})"
            else:
                self.monto -= self.monto_temporal
                resultado = "PERDIO"
                color = "#f38ba8"
                mensaje = f"Ronda {self.ronda}: Perdió (-${self.monto_temporal})"

        # --- SE INSERTA CADA RONDA EN LA LISTA DOBLEMENTE ENLAZADA ---
        self.historial.insertar([self.ronda, self.valor_elegido, valor_elegido2, self.monto_temporal, resultado, self.monto])
        
        self.actualizar_grafica(color)
        self.valor_elegido = valor_elegido2

        self.lbl_monto.config(text=f"${self.monto}")
        self.lbl_valor_actual.config(text=str(self.valor_elegido))
        self.txt_logs.insert(tk.END, mensaje + f" -> Saldo: ${self.monto}\n")
        self.txt_logs.see(tk.END)

        if self.monto <= 0:
            messagebox.showerror("Fin del juego", "¡Te has quedado sin fondos!")
            self.root.quit()
        elif self.monto < self.monto_temporal:
            messagebox.showwarning("Atención", "Saldo menor a la apuesta. Cámbiala.")
            self.cambiar_apuesta()

    def cambiar_apuesta(self):
        nuevo = simpledialog.askinteger("Cambiar Apuesta", f"Saldo disponible: ${self.monto}\nIngrese nuevo monto:", minvalue=1, maxvalue=self.monto)
        if nuevo is not None:
            self.monto_temporal = nuevo
            self.lbl_apuesta.config(text=f"${self.monto_temporal}")

    def mostrar_ventana_historial(self):
        """Abre una ventana visual interactiva que recorre la Lista Doblemente Enlazada."""
        ventana_hist = tk.Toplevel(self.root)
        ventana_hist.title("Gestión de Historial - Lista Doblemente Enlazada")
        ventana_hist.geometry("600x500")
        ventana_hist.config(bg="#1e1e2e")

        tk.Label(ventana_hist, text="Contenido de la Lista Doblemente Enlazada (Adelante y Atrás)", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack(pady=10)

        txt_hist = tk.Text(ventana_hist, font=("Consolas", 9), bg="#181825", fg="#cdd6f4", padx=10, pady=10, bd=0)
        txt_hist.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Obtenemos los datos directamente de la lista doblemente enlazada
        contenido_normal = self.historial.obtener_historial_texto()
        contenido_inverso = self.historial.obtener_historial_inverso()
        
        txt_hist.insert(tk.END, contenido_normal + "\n\n" + contenido_inverso)

        def eliminar_nodo_ronda():
            num = simpledialog.askinteger("Eliminar", "Ingrese el número de ronda a eliminar de la lista:", parent=ventana_hist)
            if num is not None:
                if self.historial.eliminar(num):
                    messagebox.showinfo("Éxito", f"Ronda {num} eliminada correctamente de la lista.", parent=ventana_hist)
                    txt_hist.delete("1.0", tk.END)
                    txt_hist.insert(tk.END, self.historial.obtener_historial_texto() + "\n\n" + self.historial.obtener_historial_inverso())
                else:
                    messagebox.showerror("Error", f"No se encontró la ronda {num} en la lista.", parent=ventana_hist)

        btn_eliminar = tk.Button(ventana_hist, text="🗑️ Eliminar una Ronda por Número", bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, pady=6, command=eliminar_nodo_ronda)
        btn_eliminar.pack(pady=15)


# --- FLUJO DE CONSOLA (REGISTRO INICIAL) ---
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
        root = tk.Tk()
        app = SimuladorInversionesApp(root, nombre, MONTO_INICIAL)
        root.mainloop()


if __name__ == "__main__":
    main()
