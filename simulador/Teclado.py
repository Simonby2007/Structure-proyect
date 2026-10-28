"""Espera con tiempo límite que se puede cancelar pulsando la tecla ESC.

Funciona en Windows (msvcrt) y en Linux/macOS (termios). Hay que ejecutarlo
desde una terminal real: si la entrada no es interactiva (por ejemplo, la
consola de algunos IDE) solo espera el tiempo completo y avisa de que ESC no
se puede detectar.
"""
import sys
import time
from contextlib import contextmanager, nullcontext

ESC = "\x1b"
PASO = 0.05  # segundos entre cada comprobación

if sys.platform == "win32":
    import msvcrt

    def _vaciar():
        while msvcrt.kbhit():
            msvcrt.getwch()

    @contextmanager
    def _modo_teclas():
        _vaciar()  # ignora lo que se haya tecleado antes
        try:
            yield
        finally:
            _vaciar()  # y lo que se teclee durante la espera

    def _leer_tecla(timeout):
        fin = time.monotonic() + timeout
        while True:
            if msvcrt.kbhit():
                return msvcrt.getwch()
            if time.monotonic() >= fin:
                return None
            time.sleep(0.01)

else:
    import os
    import select
    import termios
    import tty

    def _vaciar():
        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)

    @contextmanager
    def _modo_teclas():
        fd = sys.stdin.fileno()
        original = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)  # una tecla a la vez, sin eco y sin Enter
            _vaciar()
            yield
        finally:
            _vaciar()
            termios.tcsetattr(fd, termios.TCSADRAIN, original)

    def _leer_tecla(timeout):
        fd = sys.stdin.fileno()
        listo, _, _ = select.select([fd], [], [], timeout)
        if not listo:
            return None
        datos = os.read(fd, 32)
        # Las flechas y otras teclas especiales envían ESC seguido de más
        # bytes; solo un ESC solo cuenta como la tecla ESC.
        return datos.decode(errors="ignore")


def _dormir(timeout):
    time.sleep(timeout)
    return None


_avisado = False


def _avisar_sin_teclado():
    global _avisado
    if not _avisado:
        print("(Aviso: esta consola no permite detectar teclas, así que ESC no "
              "funcionará. Ejecuta el programa desde una terminal.)")
        _avisado = True


def esperar_esc(segundos, al_esperar=None):
    """Espera hasta `segundos`. Devuelve True si se pulsó ESC antes de que acabe.

    `al_esperar(restante)` se llama cada ~50 ms con los segundos que faltan
    (sirve para mostrar una cuenta regresiva o refrescar una ventana).
    """
    interactivo = sys.stdin.isatty()
    if not interactivo:
        _avisar_sin_teclado()
    leer = _leer_tecla if interactivo else _dormir
    modo = _modo_teclas() if interactivo else nullcontext()

    limite = time.monotonic() + segundos
    with modo:
        while True:
            restante = limite - time.monotonic()
            if restante <= 0:
                return False
            if al_esperar is not None:
                al_esperar(restante)
            if leer(min(PASO, restante)) == ESC:
                return True
