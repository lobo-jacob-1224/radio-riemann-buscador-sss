#!/usr/bin/env python3
"""Abre el buscador SSS en Google Chrome para usar Gemini Nano (Prompt API).

Usa el perfil normal de Chrome, que es donde está descargado el modelo
(~/.config/google-chrome/OptGuideOnDeviceModel). El servidor se lanza en
segundo plano y se apaga solo tras AUTO_APAGADO segundos sin actividad.
"""
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
PUERTO = int(os.environ.get('SSS_PUERTO', 5000))
URL = f"http://127.0.0.1:{PUERTO}/"
AUTO_APAGADO = 600
ESPERA_MAX = 120
LOG = os.path.join(os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache')), 'sss-browser', 'servidor.log')


def servidor_activo():
    """True only if the program answering on the port is the SSS server (/api/estado)."""
    try:
        with urllib.request.urlopen(URL + 'api/estado', timeout=1) as resp:
            return json.load(resp).get('servicio') == 'sss-buscador'
    except (OSError, ValueError):
        return False


def servidor_gestionado():
    """True if systemd's sss-browser-2.socket holds the port: systemd then starts the server
    itself on the first connection, so no second server must be launched here."""
    try:
        return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', 'sss-browser-2.socket'],
                              timeout=5).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def lanzar_servidor():
    """Start servidor_mono.py in the background and return its process without waiting."""
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'a') as log:
        return subprocess.Popen(
            [sys.executable, os.path.join(DIR, 'servidor_mono.py'), str(PUERTO),
             '--auto-apagado', str(AUTO_APAGADO)],
            cwd=DIR, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
            start_new_session=True)


def arrancar_servidor():
    proc = None if servidor_gestionado() else lanzar_servidor()
    fin = time.monotonic() + ESPERA_MAX
    while time.monotonic() < fin:
        if servidor_activo():
            return
        if proc is not None and proc.poll() is not None:
            sys.exit(f"El servidor SSS terminó con código {proc.returncode}. Revisa {LOG}")
        time.sleep(0.5)
    sys.exit(f"El servidor SSS no respondió en {ESPERA_MAX} s. Revisa {LOG}")


def buscar_chrome():
    for nombre in ('google-chrome', 'google-chrome-stable', '/opt/google/chrome/chrome'):
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    sys.exit("No se encontró Google Chrome. Gemini Nano solo funciona dentro de Chrome.")


def main():
    if not servidor_activo():
        print("Iniciando servidor SSS (carga de MiniLM)…")
        arrancar_servidor()
    subprocess.Popen([buscar_chrome(), f'--app={URL}', '--class=sss-browser'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


if __name__ == '__main__':
    main()
