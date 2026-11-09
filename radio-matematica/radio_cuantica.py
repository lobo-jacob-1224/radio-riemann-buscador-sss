#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
📡 RADIO CUÁNTICA: EL GENIO EN VIVO 📡
================================================================================
Análisis matemático en tiempo real de flujos de música clásica.
Visualización de la Transformada de Fourier + Operadores de Riemann.

Jacobo Cánovas García & AI (Zencoder)
================================================================================
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import subprocess
import threading
import time
import locale
import random
from motor_convergencia_infinito import MotorConvergencia

# Estandarización
try:
    locale.setlocale(locale.LC_NUMERIC, 'C')
except:
    pass

class RadioCuantica: # Clase maestra para la gestión de la Radio Cuántica
    def __init__(self, root): # Constructor de la interfaz y el motor de flujo
        self.root = root # Anclaje de la ventana principal de Tkinter
        self.root.title("📡 RADIO CUÁNTICA - Matemática en Vivo") # Definición del título de la sesión
        self.root.geometry("1600x900") # Dimensionamiento del espacio de trabajo visual
        self.root.configure(bg="#010103") # Color de fondo: negro

        # Configuración de Stream (Radio Swiss Classic)
        self.stream_url = "http://stream.srg-ssr.ch/m/rsc_de/mp3_128" # Fuente de audio de alta cultura
        self.sample_rate = 44100 # Tasa de muestreo estándar de alta fidelidad
        self.chunk_size = 2048 # Tamaño del fragmento para el análisis de Fourier
        
        # Buffers de Datos
        self.audio_data = np.zeros(self.chunk_size) # Buffer temporal para la señal de audio cruda
        self.fft_data = np.zeros(self.chunk_size // 2) # Buffer para el espectro de frecuencias analizado
        self.running = True # Flag de ejecución continua del sistema
        self.motor = MotorConvergencia(num_zeros=20) # Instanciación del motor de Riemann (20 ceros)

        self.setup_ui() # Inicialización de los componentes gráficos
        
        # Iniciar captura en hilo separado
        self.capture_thread = threading.Thread(target=self.stream_audio, daemon=True) # Hilo de captura asíncrona
        self.capture_thread.start() # Inicio de la succión de datos del stream
        
        self.animate() # Lanzamiento del motor de animación visual

    def setup_ui(self): # Configuración de la interfaz de usuario cinematográfica
        # Header
        header = tk.Frame(self.root, bg="#010103") # Contenedor superior
        header.pack(fill="x", pady=20) # Posicionamiento del header
        tk.Label(header, text="📡 RADIO CUÁNTICA", bg="#010103", fg="#ffffff", font=("Helvetica", 32, "bold")).pack() # Título principal
        tk.Label(header, text="DISENTRAÑANDO EL ADN DE LA MÚSICA CLÁSICA EN TIEMPO REAL", bg="#010103", fg="#00d4ff", font=("Courier", 10)).pack() # Subtítulo técnico

        # Monitor de Espectro (Matemática Pura)
        self.fig, (self.ax_wave, self.ax_orb) = plt.subplots(1, 2, figsize=(14, 7), facecolor='#010103') # Creación de la figura base
        
        # Gráfica de Onda (Tiempo)
        self.ax_wave.set_facecolor('#010103') # Fondo del osciloscopio
        self.line_wave, = self.ax_wave.plot([], [], color='#00ffaa', lw=1) # Línea de la onda temporal
        self.ax_wave.set_title("FLUJO TEMPORAL (ADAPTATIVO)", color="white", fontdict={'fontsize': 10}) # Título del osciloscopio
        self.ax_wave.axis('off') # Ocultación de ejes para estética minimalista

        # El Orbe (Frecuencia)
        self.ax_orb.set_facecolor('#010103') # Fondo del analizador espectral circular
        self.theta = np.linspace(0, 2*np.pi, self.chunk_size // 2) # Definición de ángulos para el orbe
        self.orb_line, = self.ax_orb.plot([], [], color='#00d4ff', lw=1.5) # Línea del orbe de Fourier
        self.ax_orb.set_title("EL ORBE DE FOURIER", color="white", fontdict={'fontsize': 10}) # Título del orbe
        self.ax_orb.axis('off') # Ocultación de ejes

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root) # Integración de Matplotlib en Tkinter
        self.canvas.get_tk_widget().pack(expand=True, fill="both") # Empaquetado del canvas

        # Terminal de Datos
        self.log_feed = tk.Text(self.root, bg="#010103", fg="#004433", font=("Courier", 9), height=5, bd=0) # HUD de telemetría
        self.log_feed.pack(fill="x", padx=50, pady=20) # Posicionamiento del HUD

    def stream_audio(self): # Función de gestión del flujo de audio y rectificación
        """Captura el stream de radio, lo analiza y lo reproduce en tiempo real (ESTÉREO BINAURAL S3)"""
        cmd_in = [ # Comando FFMPEG para la captura del stream
            'ffmpeg', '-i', self.stream_url,
            '-f', 's16le', '-ac', '2', '-ar', str(self.sample_rate), '-'
        ]
        process_in = subprocess.Popen(cmd_in, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) # Ejecución del proceso de captura
        
        # Tubería de salida hacia los altavoces
        try: # Intento de apertura del dispositivo de salida de audio ESTÉREO
            process_out = subprocess.Popen(['pw-play', '-a', '--rate', str(self.sample_rate), '--format', 's16', '--channels', '2', '-'], 
                                         stdin=subprocess.PIPE, stderr=subprocess.DEVNULL) # Reproducción vía PipeWire
        except: # Manejo de error en la salida de audio
            print("❌ Error al iniciar salida de audio (aplay).") # Notificación de fallo
            process_out = None # Anulación del proceso de salida

        while self.running: # Bucle principal de procesamiento de audio
            raw_data = process_in.stdout.read(self.chunk_size * 4) # Lectura de datos binarios del stream (Estéreo 4 bytes)
            if not raw_data: break # Salida si el stream se corta
            
            # 1. Motor de Riemann
            data_int16 = np.frombuffer(raw_data, dtype=np.int16)
            # Reshape Estéreo (N, 2)
            data_stereo = data_int16.reshape(-1, 2).astype(np.float32) / 32768.0 
            
            # Aplicación de la verdad matemática Riemann (Binaural Offset en canal Derecho)
            rectificado = self.motor.rectificar_riemann(data_stereo, fs=self.sample_rate) 
            
            # Limitar y convertir
            rectificado = np.clip(rectificado, -1.0, 1.0)
            raw_rectificado = (rectificado * 32767).astype(np.int16).tobytes() # Reconversión a binario para reproducción

            # 2. Enviar a los altavoces inmediatamente
            if process_out: # Si el proceso de salida está activo
                try: # Intento de escritura en la tubería de audio
                    process_out.stdin.write(raw_rectificado) # Inyección del audio rectificado
                    process_out.stdin.flush() # Vaciado del buffer de salida
                except: pass # Silenciar errores de tubería rota
            
            # 3. Convertir a numpy para análisis visual (MONO DOWNMIX)
            mono_mix = np.mean(rectificado, axis=1) # Mezcla S1 para visualización
            
            if len(mono_mix) == self.chunk_size: # Verificación del tamaño del fragmento
                self.audio_data = mono_mix # Almacenamiento para la onda temporal
                # Calcular Matemática (FFT)
                fft = np.abs(np.fft.fft(mono_mix)[:self.chunk_size // 2]) # Cálculo de la Transformada Rápida de Fourier
                self.fft_data = fft / (np.max(fft) + 1e-6) # Normalización del espectro para visualización

    def animate(self): # Función de actualización de los visualizadores
        def update(frame): # Función interna de actualización de fotogramas
            # Actualizar Onda
            self.line_wave.set_data(np.arange(self.chunk_size), self.audio_data) # Inyección de datos en la onda temporal
            self.ax_wave.set_xlim(0, self.chunk_size) # Ajuste del dominio temporal
            self.ax_wave.set_ylim(-1, 1) # Ajuste del rango de amplitud

            # Actualizar Orbe (Matemática de Frecuencia)
            r = 1.0 + self.fft_data * 1.5 # Cálculo del radio basado en la energía espectral
            x = r * np.cos(self.theta) # Transformada de coordenadas polares a rectangulares (X)
            y = r * np.sin(self.theta) # Transformada de coordenadas polares a rectangulares (Y)
            self.orb_line.set_data(x, y) # Inyección de datos en el orbe
            self.ax_orb.set_xlim(-3, 3) # Ajuste del dominio espacial del orbe
            self.ax_orb.set_ylim(-3, 3) # Ajuste del rango espacial del orbe

            if frame % 20 == 0: # Actualización periódica de la telemetría (cada 20 frames)
                self.log_feed.insert("1.0", f"[ANALYSIS] Dominant_Freq: {np.argmax(self.fft_data) * (self.sample_rate/self.chunk_size):.2f}Hz | Energy: {np.sum(self.fft_data):.4f}\n") # Inserción de datos analíticos
                self.log_feed.delete("6.0", "end") # Limpieza del histórico del HUD

            return self.line_wave, self.orb_line # Devolución de los objetos actualizados

        self.ani = FuncAnimation(self.fig, update, interval=30, blit=True) # Creación de la animación continua
        self.canvas.draw() # Dibujado inicial del canvas

if __name__ == "__main__": # Punto de entrada del script
    root = tk.Tk() # Instanciación de la raíz de Tkinter
    app = RadioCuantica(root) # Creación de la aplicación Radio Cuántica
    root.mainloop() # Inicio del bucle de eventos de la interfaz

