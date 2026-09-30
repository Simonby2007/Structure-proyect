# Simulador de Inversiones con Análisis Gráfico e Historial

Programa en Python que simula una plataforma de apuestas e inversiones basada en la predicción de números aleatorios. El proyecto utiliza una Lista Doblemente Enlazada personalizada para gestionar el historial de jugadas y la librería Matplotlib para renderizar los resultados en tiempo real.

---

## Componentes Internos (`main.py`)

- Módulo de Registro y Autenticación:
  Captura el nombre del usuario y valida que la contraseña coincida con su confirmación antes de permitir el acceso al sistema.

- Estructura de Datos (Lista Doblemente Enlazada):
  - `Nodo`: Almacena la información de la jugada (`[ronda, valor_anterior, valor_nuevo, apuesta, resultado, saldo]`) junto con los punteros `siguiente` y `anterior`.
  - `ListaDoblementeEnlazada`: Implementación mediante nodos centinela (`cabeza` y `cola`) que incluye los métodos:
    - `insertar()`: Añade un nuevo registro al final de la lista.
    - `mostrar()`: Recorre los nodos desde el inicio hacia el final.
    - `mostrar_regreso()`: Recorre los nodos en sentido inverso (del más reciente al más antiguo).
    - `eliminar()`: Desvincula un nodo específico buscando por número de ronda.

- Validación de Entradas:
  - `pedir_entero()`: Garantiza que el usuario ingrese números enteros positivos.
  - `pedir_apuesta()`: Controla que el monto apostado no supere el saldo disponible en la cuenta.

- Visualización Gráfica (`matplotlib`):
  - Inicializa una figura interactiva (`plt.ion()`) con ejes X (Ronda) y Y (Número generado).
  - `actualizar_grafica()`: Redibuja la línea de tendencias y agrega puntos de colores según el resultado obtenido (Verde: Ganó, Rojo: Perdió, Naranja: Empate, Azul: Inicio).

- Bucle Principal del Juego:
  - Permite seleccionar la predicción (`1`: MAYOR, `2`: MENOR), ajustar la apuesta (`3`), acceder al menú del historial (`4`) o terminar la partida (`exit`).
  - Evalúa la lógica de ganancia o pérdida, actualiza el saldo del jugador y valida condiciones de bancarrota.

- Menú de Historial y Reporte Final:
  - Despliega una interfaz dedicada dentro del juego para consultar o modificar el historial en tiempo real.
  - Genera un resumen final con el total de rondas jugadas, ganadas y el porcentaje general de aciertos.

---

## Requisitos y Configuración

- `requirements.txt`: Define la dependencia externa requerida (`matplotlib`).
- `.gitignore`: Excluye del control de versiones los archivos ejecutables, entornos virtuales (`venv/`) y caché de Python (`__pycache__/`).

---

## Instrucciones de Uso

1. Clonar el repositorio.
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Ejecutar el programa: `python main.py`
