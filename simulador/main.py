# simulador/main.py

import random
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from Cola import ColaLinealEstatica
from Pila import Pila
from Teclado import esperar_esc  # <--- Importamos tu módulo de teclado


class SimuladorInversionesApp:
    def __init__(self, root, nombre_usuario, monto_inicial):
        self.root = root
        self.nombre_usuario = nombre_usuario
        self.monto = monto_inicial
        
        self.root.title(f"Simulador Pro | Usuario: {self.nombre_usuario}")
        self.root.geometry("1000x820")
        self.root.config(bg="#1e1e2e")

        # Estructuras de datos principales
        self.historial = ListaDoblementeEnlazada()
        self.cola_transacciones = ColaLinealEstatica()
        self.pila_acciones = Pila() 
        self.contador_tx = 101

        self.numeros = []
        self.ronda = 0
        self.monto_temporal = 100
        self.valor_elegido = random.randint(1, 100)
        self.numeros.append(self.valor_elegido)

        # Rellenar cola inicial con algunas transacciones de prueba opcionales
        for _ in range(3):
            self.cola_transacciones.insertar({
                "id": f"TX-{self.contador_tx}",
                "tipo": "BONO",
                "monto": 50,
                "descripcion": "Bono inicial de liquidez"
            })
            self.contador_tx += 1

        self.crear_interfaz()

    def crear_interfaz(self):
        # Encabezado
        header_frame = tk.Frame(self.root, bg="#252538", pady=10)
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame, text=f"📈 SIMULADOR (Lista, Cola y Pila integradas)", 
            font=("Segoe UI", 12, "bold"), fg="#cdd6f4", bg="#252538"
        ).pack()

        # Tarjetas Superiores
        info_frame = tk.Frame(self.root, bg="#1e1e2e", pady=6)
        info_frame.pack(fill=tk.X, padx=15)

        card_monto = tk.Frame(info_frame, bg="#313244", padx=15, pady=6)
        card_monto.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(card_monto, text="MONTO DISPONIBLE", font=("Segoe UI", 8), fg="#a6adc8", bg="#313244").pack(anchor="w")
        self.lbl_monto = tk.Label(card_monto, text=f"${self.monto}", font=("Segoe UI", 12, "bold"), fg="#a6e3a1", bg="#313244")
        self.lbl_monto.pack(anchor="w")

        card_inv = tk.Frame(info_frame, bg="#313244", padx=15, pady=6)
        card_inv.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(card_inv, text="INVERSIÓN", font=("Segoe UI", 8), fg="#a6adc8", bg="#313244").pack(anchor="w")
        self.lbl_apuesta = tk.Label(card_inv, text=f"${self.monto_temporal}", font=("Segoe UI", 12, "bold"), fg="#89b4fa", bg="#313244")
        self.lbl_apuesta.pack(anchor="w")

        card_val = tk.Frame(info_frame, bg="#313244", padx=15, pady=6)
        card_val.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Label(card_val, text="VALOR REFERENCIA", font=("Segoe UI", 8), fg="#a6adc8", bg="#313244").pack(anchor="w")
        self.lbl_valor_actual = tk.Label(card_val, text=str(self.valor_elegido), font=("Segoe UI", 12, "bold"), fg="#fab387", bg="#313244")
        self.lbl_valor_actual.pack(anchor="w")

        # --- PANEL DE COLA ESTÁTICA (FIFO) VISIBLE EN LA INTERFAZ ---
        cola_frame = tk.Frame(self.root, bg="#252538", padx=12, pady=6)
        cola_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(cola_frame, text="💳 Cola Estática de Movimientos de Dinero Pendientes (FIFO):", font=("Segoe UI", 9, "bold"), fg="#f9e2af", bg="#252538").pack(anchor="w")
        
        # Como los elementos de la cola son diccionarios, creamos una función para mostrar sus IDs de forma limpia
        self.lbl_estado_cola = tk.Label(cola_frame, text=self.obtener_texto_cola(), font=("Consolas", 10), fg="#89b4fa", bg="#252538")
        self.lbl_estado_cola.pack(anchor="w", pady=2)

        btn_procesar_tx = tk.Button(cola_frame, text="⚙️ Procesar Siguiente Movimiento (Liquidar Dinero)", font=("Segoe UI", 8, "bold"), bg="#a6e3a1", fg="#1e1e2e", relief=tk.FLAT, command=self.procesar_transaccion)
        btn_procesar_tx.pack(side=tk.LEFT, padx=2)

        # Cuerpo Principal
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Panel Izquierdo
        left_panel = tk.Frame(main_frame, bg="#252538", padx=15, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        tk.Label(left_panel, text="¿El próximo número será?", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#252538").pack(anchor="w", pady=(0, 6))

        btn_mayor = tk.Button(left_panel, text="📈 MAYOR (Con Pausa ESC)", font=("Segoe UI", 9, "bold"), bg="#a6e3a1", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=24, pady=5, command=lambda: self.jugar_con_espera("1"))
        btn_mayor.pack(pady=3)

        btn_menor = tk.Button(left_panel, text="📉 MENOR (Con Pausa ESC)", font=("Segoe UI", 9, "bold"), bg="#f38ba8", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=24, pady=5, command=lambda: self.jugar_con_espera("2"))
        btn_menor.pack(pady=3)

        tk.Frame(left_panel, height=2, bg="#313244", bd=0).pack(fill=tk.X, pady=6)

        btn_deshacer = tk.Button(left_panel, text="🔄 Deshacer Última Jugada (Pila)", font=("Segoe UI", 9, "bold"), bg="#fab387", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=24, pady=5, command=self.deshacer_jugada)
        btn_deshacer.pack(pady=3)

        btn_cambiar = tk.Button(left_panel, text="💵 Cambiar Apuesta", font=("Segoe UI", 9), bg="#89b4fa", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=24, pady=4, command=self.cambiar_apuesta)
        btn_cambiar.pack(pady=3)

        btn_historial = tk.Button(left_panel, text="📜 Ver Historial (Lista)", font=("Segoe UI", 9), bg="#cba6f7", fg="#1e1e2e", relief=tk.FLAT, cursor="hand2", width=24, pady=4, command=self.mostrar_ventana_historial)
        btn_historial.pack(pady=3)

        btn_salir = tk.Button(left_panel, text="❌ Salir", font=("Segoe UI", 9), bg="#45475a", fg="#cdd6f4", relief=tk.FLAT, cursor="hand2", width=24, pady=4, command=self.root.quit)
        btn_salir.pack(pady=(8, 0))

        # Consola de eventos
        tk.Label(left_panel, text="Registro de jugadas:", font=("Segoe UI", 8, "bold"), fg="#a6adc8", bg="#252538").pack(anchor="w", pady=(6, 2))
        self.txt_logs = tk.Text(left_panel, height=6, width=28, font=("Consolas", 8), bg="#181825", fg="#cdd6f4", bd=0, padx=5, pady=5)
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

    def obtener_texto_cola(self):
        """Genera la representación visual de los elementos guardados en la cola estática."""
        if self.cola_transacciones.esta_vacia():
            return "[ Cola de Movimientos Vacía ]"

        texto = ""
        actual = self.cola_transacciones.cabeza.siguiente
        while actual is not self.cola_transacciones.cola:
            item = actual.info
            if isinstance(item, dict):
                texto += f"[{item['id']}] "
            else:
                texto += f"[{item}] "
            actual = actual.siguiente
        return texto

    # --- MÉTODOS DE LA COLA (LIQUIDACIÓN DE DINERO FIFO) ---
    def procesar_transaccion(self):
        """
        Saca el movimiento financiero del frente de la cola (FIFO) y aplica
        efectivamente el cambio al saldo disponible del usuario.
        """
        if self.cola_transacciones.esta_vacia():
            messagebox.showinfo("Cola Vacía", "⚠️ No hay movimientos de dinero pendientes en la Cola.")
            return
        
        tx = self.cola_transacciones.eliminar()
        self.lbl_estado_cola.config(text=self.obtener_texto_cola())

        # Si es un bono o recarga inicial
        if tx.get("tipo") == "BONO":
            self.monto += tx["monto"]
            self.lbl_monto.config(text=f"${self.monto}")
            self.txt_logs.insert(tk.END, f"💰 Movimiento {tx['id']} liquidado: +${tx['monto']} ({tx['descripcion']}). Saldo: ${self.monto}\n")
            self.txt_logs.see(tk.END)
            messagebox.showinfo("Bono Liquidado", f"Se ha aplicado el movimiento {tx['id']}: +${tx['monto']}")
            return

        # Si es el resultado financiero de una partida jugada
        monto_movimiento = tx["monto_efecto"]
        tipo_resultado = tx["resultado"]
        id_tx = tx["id"]

        self.monto += monto_movimiento
        self.lbl_monto.config(text=f"${self.monto}")
        
        signo = "+" if monto_movimiento >= 0 else ""
        self.txt_logs.insert(tk.END, f"⚙️ Liquidado {id_tx} ({tipo_resultado}): {signo}${monto_movimiento} -> Saldo: ${self.monto}\n")
        self.txt_logs.see(tk.END)

        messagebox.showinfo("Movimiento Liquidado", f"Transacción {id_tx} procesada.\nResultado: {tipo_resultado} ({signo}${monto_movimiento})\nNuevo Saldo: ${self.monto}")

        if self.monto <= 0:
            messagebox.showerror("Fin del juego", "¡Te has quedado sin fondos!")
            self.root.quit()

    def jugar_con_espera(self, comparacion):
        """Lanza la espera en un hilo secundario para usar Teclado.py sin congelar la interfaz."""
        if self.monto <= 0:
            messagebox.showwarning("Game Over", "Sin fondos disponibles.")
            return
        
        self.txt_logs.insert(tk.END, "⏳ Analizando mercado... Presiona ESC en la terminal para cancelar.\n")
        self.txt_logs.see(tk.END)

        def proceso_espera():
            cancelado = esperar_esc(3.0, al_esperar=lambda r: print(f"Tiempo restante para resolver jugada: {r:.1f}s (Pulsa ESC para cancelar)"))
            self.root.after(0, lambda: self.finalizar_jugada(comparacion, cancelado))

        threading.Thread(target=proceso_espera, daemon=True).start()

    def finalizar_jugada(self, comparacion, cancelado):
        if cancelado:
            self.txt_logs.insert(tk.END, "⚠️ ¡Jugada CANCELADA por el usuario (Tecla ESC)!\n")
            self.pila_acciones.push({"tipo": "CANCELADA", "monto": self.monto})
            return

        estado_previo = {
            "monto": self.monto,
            "ronda": self.ronda,
            "valor_elegido": self.valor_elegido,
            "numeros_len": len(self.numeros)
        }
        self.pila_acciones.push(estado_previo)

        # 1. EL JUEGO OCURRE AL INSTANTE
        valor_elegido2 = random.randint(1, 100)
        self.ronda += 1
        self.numeros.append(valor_elegido2)
        resultado = ""
        color = "#89b4fa"
        monto_efecto = 0  # Dinero que afectará el saldo después

        if valor_elegido2 == self.valor_elegido:
            resultado = "EMPATE"
            color = "#fab387"
            monto_efecto = 0
            mensaje = f"Ronda {self.ronda}: Empate ({valor_elegido2}). Sin cambio en saldo."
        else:
            acerto = (comparacion == "1" and valor_elegido2 > self.valor_elegido) or \
                     (comparacion == "2" and valor_elegido2 < self.valor_elegido)
            if acerto:
                monto_efecto = self.monto_temporal
                resultado = "GANO"
                color = "#a6e3a1"
                mensaje = f"Ronda {self.ronda}: ¡Ganó! (+${self.monto_temporal} pendiente en cola)"
            else:
                monto_efecto = -self.monto_temporal
                resultado = "PERDIO"
                color = "#f38ba8"
                mensaje = f"Ronda {self.ronda}: Perdió (-${self.monto_temporal} pendiente en cola)"

        # 2. GUARDAMOS EN EL HISTORIAL (Lista Doblemente Enlazada)
        self.historial.insertar([self.ronda, self.valor_elegido, valor_elegido2, self.monto_temporal, resultado, self.monto])
        self.actualizar_grafica(color)
        self.valor_elegido = valor_elegido2
        self.lbl_valor_actual.config(text=str(self.valor_elegido))

        # 3. ENCOLAMOS EL MOVIMIENTO FINANCIERO (En vez de aplicarlo al saldo de una vez)
        id_tx = f"TX-{self.contador_tx}"
        movimiento_financiero = {
            "id": id_tx,
            "tipo": "PARTIDA",
            "resultado": resultado,
            "monto_efecto": monto_efecto
        }
        
        exito = self.cola_transacciones.insertar(movimiento_financiero)
        if exito:
            self.contador_tx += 1
            self.lbl_estado_cola.config(text=self.obtener_texto_cola())

        self.txt_logs.insert(tk.END, mensaje + f" -> [Movimiento {id_tx} encolado]\n")
        self.txt_logs.see(tk.END)

    def deshacer_jugada(self):
        if self.pila_acciones.esta_vacia():
            messagebox.showinfo("Pila Vacía", "⚠️ No hay acciones previas en la Pila para deshacer.")
            return

        estado_anterior = self.pila_acciones.pop()

        if isinstance(estado_anterior, dict) and estado_anterior.get("tipo") == "CANCELADA":
            self.txt_logs.insert(tk.END, "🔄 Se desapiló el registro de la jugada cancelada.\n")
            return

        self.monto = estado_anterior["monto"]
        self.ronda = estado_anterior["ronda"]
        self.valor_elegido = estado_anterior["valor_elegido"]
        self.numeros = self.numeros[:estado_anterior["numeros_len"]]

        self.lbl_monto.config(text=f"${self.monto}")
        self.lbl_valor_actual.config(text=str(self.valor_elegido))
        
        self.ax.clear()
        self.ax.set_facecolor('#181825')
        self.linea, = self.ax.plot(range(len(self.numeros)), self.numeros, color="#89b4fa", linewidth=1.5)
        if len(self.numeros) > 0:
            self.ax.scatter(len(self.numeros)-1, self.numeros[-1], color="#fab387", zorder=3, s=35)
        self.ax.set_xlim(-0.5, max(10, len(self.numeros)))
        self.ax.set_ylim(0, 101)
        self.ax.set_title("Evolución de Tendencia (Deshecho)", fontsize=10, color="#cdd6f4", pad=10)
        self.canvas.draw()

        self.txt_logs.insert(tk.END, f"🔄 Acción deshecha con éxito desde la Pila.\n")
        self.txt_logs.see(tk.END)

    def cambiar_apuesta(self):
        nuevo = simpledialog.askinteger("Cambiar Apuesta", f"Saldo disponible: ${self.monto}\nIngrese nuevo monto:", minvalue=1, maxvalue=self.monto)
        if nuevo is not None:
            self.monto_temporal = nuevo
            self.lbl_apuesta.config(text=f"${self.monto_temporal}")

    def mostrar_ventana_historial(self):
        ventana_hist = tk.Toplevel(self.root)
        ventana_hist.title("Gestión de Historial - Lista Doblemente Enlazada")
        ventana_hist.geometry("600x500")
        ventana_hist.config(bg="#1e1e2e")

        tk.Label(ventana_hist, text="Contenido de la Lista Doblemente Enlazada", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack(pady=10)

        txt_hist = tk.Text(ventana_hist, font=("Consolas", 9), bg="#181825", fg="#cdd6f4", padx=10, pady=10, bd=0)
        txt_hist.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        txt_hist.insert(tk.END, self.historial.obtener_historial_texto() + "\n\n" + self.historial.obtener_historial_inverso())

        def eliminar_nodo_ronda():
            num = simpledialog.askinteger("Eliminar", "Ingrese el número de ronda a eliminar:", parent=ventana_hist)
            if num is not None:
                if self.historial.eliminar(num):
                    messagebox.showinfo("Éxito", f"Ronda {num} eliminada.", parent=ventana_hist)
                    txt_hist.delete("1.0", tk.END)
                    txt_hist.insert(tk.END, self.historial.obtener_historial_texto() + "\n\n" + self.historial.obtener_historial_inverso())
                else:
                    messagebox.showerror("Error", f"No se encontró la ronda {num}.", parent=ventana_hist)

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
