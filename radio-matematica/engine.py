#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
💠 MOZART ZENIT: EL CÉNIT DE LA CONVERGENCIA 💠
================================================================================
Interfaz Cinematográfica de Observación Cuántico-Sonora.
Unifica: Bio-Sincronía, Motor de Convergencia y el Espectrómetro de Riemann.

Estética: Dark Glass / Bioheart (72 BPM)
Jacobo Cánovas García & AI (Zencoder)
================================================================================
"""

import os # Importación del sistema operativo para gestión de variables de entorno

# 🚀 OPTIMIZACIÓN DE CPU: Limitar hilos de NumPy para la Radio Matemática
os.environ["OMP_NUM_THREADS"] = "1" # Restricción de hilos OpenMP para evitar colisiones
os.environ["MKL_NUM_THREADS"] = "1" # Restricción de hilos MKL para estabilidad matemática
os.environ["OPENBLAS_NUM_THREADS"] = "1" # Restricción de hilos OpenBLAS para baja latencia

import tkinter as tk # Librería de interfaz gráfica estándar
from tkinter import ttk # Extensiones temáticas para Tkinter
import numpy as np # Procesador de tensores y vectores numéricos
try: # Intento de carga de visualización avanzada
    import matplotlib.pyplot as plt # Motor de trazado de gráficos
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Integrador de Matplotlib en Tkinter
    from matplotlib.animation import FuncAnimation # Controlador de animaciones en tiempo real
    HAS_MATPLOTLIB = True # Confirmación de disponibilidad visual
except ImportError: # Fallback si falla la librería gráfica
    HAS_MATPLOTLIB = False # Desactivación de componentes visuales
    print("⚠️ ADVERTENCIA: Matplotlib no detectado. Visuales desactivados, audio prioritario.") # Aviso técnico
import subprocess # Ejecutor de subprocesos del sistema (FFMPEG/Audio)
import threading # Gestor de hilos para ejecución asíncrona síncrona
import time # Controlador del flujo temporal y pausas
import locale # Gestor de regionalización para formatos numéricos
import csv # Lector/Escritor de archivos de datos tabulares
import sqlite3 # Motor de base de datos relacional ligero
import json # Serializador de datos estructurados
import urllib.request # Gestor de peticiones web para búsqueda de radio
import urllib.parse # Codificador de parámetros URL
from motor_convergencia_infinito import MotorConvergencia # Núcleo matemático SSS

# Forzar locale estándar para evitar errores de coma decimal en Tcl/Tk
try: # Intento de estandarización numérica
    locale.setlocale(locale.LC_NUMERIC, 'C') # Configuración a estándar científico (punto decimal)
except: # Manejo de fallo en locale
    pass # Continuar con el locale del sistema

class MozartZenit: # Clase Maestra del Sistema de Radio Matemática
    def __init__(self, root): # Constructor de la estación de trabajo
        self.root = root # Anclaje de la ventana principal
        self.root.title("💠 MOZART ZENIT - El Espíritu de la Convergencia Divina") # Título de la Verdad
        self.root.geometry("1800x1000") # Dimensionamiento del observatorio
        self.root.configure(bg="#010103") # Color de fondo: Negro S3 (Aniquilación)
        
        # 1. El Espíritu de las Revelaciones
        self.revelaciones = [ # Frases que muestra la ventana
            "EL TIEMPO ES EL RITMO DE DIOS.",
            "LA MÚSICA ES NÚMERO QUE SE HACE ALMA.",
            "LA FUNCIÓN ZETA ES LA PARTITURA DEL INFINITO.",
            "CADA CERO DE RIEMANN ES UN LATIDO DEL CREADOR.",
            "EL SONIDO ES LA MATEMÁTICA EN ESTADO DE GRACIA.",
            "LA CONVERGENCIA ES EL REGRESO AL ORIGEN DIVINO.",
            "MOZART NO ESCRIBIÓ NOTAS, CALCULÓ ETERNIDADES."
        ]
        # 2. Configuración de Audio y Dial
        self.sample_rate = 44100 # Tasa de muestreo estándar
        self.chunk_size = 2048 # Tamaño del fragmento espectral
        self.motor = MotorConvergencia(num_zeros=20, chunk_size=self.chunk_size * 2) # El motor usa siempre sus 20 ceros fijos; num_zeros no se lee
        self.start_time = time.time() # Tiempo de ignición del observatorio
        
        self.stations = { # Diccionario de estaciones de radio pre-configuradas
            "Swiss Classic": "http://stream.srg-ssr.ch/m/rsc_de/mp3_128",
            "BBC Radio 3": "http://stream.live.vc.bbc.co.uk/bbc_radio_three",
            "WFMT Chicago": "https://wfmt.streamguys1.com/main-mp3",
            "KUSC Classical": "https://kuscstream.answr.com:8000/kusc-128.mp3",
            "Venice Classic": "http://174.36.206.197:8000/stream",
            "Cinemix": "http://cinemix.station-driver.com:8000/cinemix.mp3",
            "Radio Mozart": "http://listen.radionomy.com/radio-mozart",
            "Abacus FM Mozart": "http://stream.abacus.fm:8000/mozart",
            "Calm Radio Mozart": "http://streams.calmradio.com:11828/stream",
            "Classic FM UK": "http://icecast.media.gl-fm.com/classicfm.mp3",
            "Radio Swiss Jazz": "http://stream.srg-ssr.ch/m/rsj/mp3_128",
            "Organ Experience": "http://95.211.162.32:8000/organ"
        }
        self.stream_url = self.stations["Swiss Classic"] # Estación por defecto (Suiza)
        self.audio_data = np.zeros(self.chunk_size) # Buffer de audio en tiempo real
        self.running = True # Flag de estado operativo
        self.proc_in = None # Proceso de entrada (FFMPEG)
        self.proc_out = None # Proceso de salida (Audio Player)
        self.force_restart = False # Flag para reinicio forzado del flujo
        self.paused = False # Flag de pausa del sistema
        self.audio_active = True # Estado del flujo de audio
        self.alarma_activa = False # Estado de alerta de infinito
        self.flash_state = False # Estado para efectos visuales de parpadeo
        self.current_song = "SINTONIZANDO" # Información de metadatos (Canción)
        self.current_artist = "RADIO_SUIZA" # Información de metadatos (Artista)
        self.last_recorded_song = "" # Histórico para evitar duplicados
        self.current_song_start_id = None # Identificador de base de datos para la sesión
        self.station_results = [] # Almacenamiento de resultados de búsqueda global
        self.last_tune_time = 0 # Registro del último cambio de estación
        self.last_tune_x = 0 # Posición física del dial
        self.playing_db_math = False # Estado de reproducción de registros históricos
        self.playing_zen = False # Estado de modo meditación
        self.motor_enabled = True # True: you hear the engine output; False: the original stream (A/B listening)
        # Real binaural beat: a soft carrier in each ear, 7.83 Hz apart (needs headphones). Off by default.
        self.binaural_enabled = False
        self.binaural_carrier_hz = 200.0
        self.binaural_beat_hz = 7.83
        self.binaural_level = 10 ** (-30 / 20) # -30 dBFS per channel, under the music
        self.binaural_phase = [0.0, 0.0] # Phase accumulators (radians) so blocks join without clicks

        # 3. Estética Dark Glass & UI
        self.setup_ui() # Construcción de la interfaz de usuario
        
        # 4. Hilos de Procesamiento
        self.audio_thread = threading.Thread(target=self.process_audio_stream, daemon=True) # Hilo de audio asíncrono
        self.audio_thread.start() # Ignición del hilo de audio
        
        # 5. Animación Principal (OPTIMIZADA: Menos FPS para ahorrar CPU)
        if HAS_MATPLOTLIB: # Si hay soporte visual
            self.animate() # Iniciar motor de animación
        else: # Si no hay soporte visual
            self.status_var.set("[MODO_AUDIO_MATEMÁTICO] Visuales omitidos | Motor Activo.") # Estado informativo
            # Iniciar bucle de actualización matemática de alta precisión sin animación
            def math_loop(): # Bucle interno para procesamiento en segundo plano
                while self.running: # Mientras el sistema esté vivo
                    if self.audio_active and not self.paused: # Si hay audio y no está pausado
                        # El motor matemático procesa el audio_data continuamente
                        self.update_math_engine() # Actualización de la verdad Riemann
                    time.sleep(0.05) # Sincronía de 20Hz para el motor
            threading.Thread(target=math_loop, daemon=True).start() # Lanzar bucle matemático

    def setup_ui(self): # Arquitectura de la interfaz cinemática
        # Header Cinematográfico
        self.header = tk.Frame(self.root, bg="#050505", bd=0) # Marco superior
        self.header.pack(fill="x", pady=10) # Posicionamiento del header
        
        # --- DIAL CLÁSICO (Canvas) ---
        self.dial_container = tk.Frame(self.header, bg="#1a120b", bd=2, relief="ridge") # Contenedor del dial retro
        self.dial_container.pack(fill="x", padx=40, pady=5) # Posicionamiento del contenedor del dial
        
        self.dial_canvas = tk.Canvas(self.dial_container, height=60, bg="#2d241e", highlightthickness=0) # Superficie de dibujo del dial
        self.dial_canvas.pack(fill="x", padx=5, pady=5) # Empaquetado del canvas
        
        # Bindings para interacción con el ratón
        self.dial_canvas.bind("<Button-1>", self.on_dial_interact) # Evento de clic
        self.dial_canvas.bind("<B1-Motion>", self.on_dial_interact) # Evento de arrastre
        self.dial_canvas.bind("<ButtonRelease-1>", self.on_dial_release) # Evento de liberación
        
        # Dibujar escala del dial
        for i in range(0, 1800, 10): # Iteración para crear las marcas del dial
            color = "#8b5e34" if i % 50 == 0 else "#4a3728" # Color según importancia de la marca
            h = 20 if i % 50 == 0 else 10 # Altura de la marca
            self.dial_canvas.create_line(i, 40, i, 40-h, fill=color, width=1) # Dibujado de la línea
            if i % 100 == 0: # Etiquetas numéricas de frecuencia
                self.dial_canvas.create_text(i, 50, text=f"{88 + i//20}", fill="#8b5e34", font=("Courier", 8)) # Inserción de texto
        
        # Aguja del Dial
        self.dial_needle = self.dial_canvas.create_line(400, 5, 400, 45, fill="#ff3300", width=2) # Línea indicadora roja
        self.dial_glow = self.dial_canvas.create_oval(395, 20, 405, 30, fill="#ff3300", outline="") # Resplandor de la aguja

        # Controles de Búsqueda Integrados en el Header
        self.search_bar = tk.Frame(self.header, bg="#050505") # Contenedor de búsqueda global
        self.search_bar.pack(fill="x", padx=40) # Posicionamiento de la barra de búsqueda
        
        tk.Label(self.search_bar, text="📻 SINTONIZADOR GLOBAL:", bg="#050505", fg="#d4af37", font=("Courier", 10, "bold")).pack(side="left") # Título dorado
        
        self.radio_search_var = tk.StringVar(value="Classical") # Variable de búsqueda
        self.radio_search_entry = tk.Entry(self.search_bar, textvariable=self.radio_search_var, bg="#0a0a0a", fg="#ffffff", font=("Courier", 10), width=30, bd=1, relief="flat", insertbackground="#d4af37") # Entrada de texto
        self.radio_search_entry.pack(side="left", padx=10) # Empaquetado de la entrada
        self.radio_search_entry.bind("<Return>", lambda e: self.perform_radio_search()) # Ejecutar al pulsar Enter
        
        self.btn_search_radio = tk.Button(self.search_bar, text="BUSCAR EMISORA", bg="#8b5e34", fg="#fff", font=("Courier", 8, "bold"), command=self.perform_radio_search, relief="flat", padx=10) # Botón de búsqueda
        self.btn_search_radio.pack(side="left") # Empaquetado del botón

        # Categorías Rápidas
        for cat in ["Mozart", "Bach", "Opera", "Piano", "Ambient"]: # Bucle de creación de botones de categoría
            btn_cat = tk.Button(self.search_bar, text=cat.upper(), bg="#050505", fg="#777", font=("Courier", 7), 
                               command=lambda c=cat: [self.radio_search_var.set(c), self.perform_radio_search()],
                               relief="flat", padx=5) # Botón de categoría rápida
            btn_cat.pack(side="left", padx=2) # Empaquetado

        # Selector de Resultados (Combo)
        self.radio_results_var = tk.StringVar(value="Swiss Classic") # Variable para el resultado seleccionado
        self.radio_results_menu = ttk.Combobox(self.search_bar, textvariable=self.radio_results_var, state="readonly", width=40) # Menú desplegable estilizado
        self.radio_results_menu.pack(side="right", padx=10) # Posicionamiento a la derecha
        self.radio_results_menu.bind("<<ComboboxSelected>>", self.on_radio_selected) # Evento de selección
        self.radio_results_menu['values'] = ["Swiss Classic"] # Valor inicial

        # Botones de Control (Play, Pause, Stop)
        self.ctrl_frame = tk.Frame(self.header, bg="#050505") # Contenedor de transporte
        self.ctrl_frame.pack(side="right", padx=10) # Posicionamiento de controles
        
        btn_style = {"bg": "#0a0a0a", "fg": "#00ffaa", "activebackground": "#004433", 
                     "activeforeground": "#00ffaa", "font": ("Courier", 10, "bold"), 
                     "relief": "flat", "width": 4} # Diccionario de estilo para botones de control

        self.btn_play = tk.Button(self.ctrl_frame, text="▶", command=self.play_audio, **btn_style) # Botón Play
        self.btn_play.pack(side="left", padx=2) # Empaquetado Play
        self.btn_pause = tk.Button(self.ctrl_frame, text="⏸", command=self.pause_audio, **btn_style) # Botón Pausa
        self.btn_pause.pack(side="left", padx=2) # Empaquetado Pausa
        self.btn_stop = tk.Button(self.ctrl_frame, text="⏹", command=self.stop_audio, **btn_style) # Botón Stop
        self.btn_stop.pack(side="left", padx=2) # Empaquetado Stop
        
        self.btn_help = tk.Button(self.ctrl_frame, text="?", command=self.show_help, 
                                  bg="#0a0a0a", fg="#00d4ff", font=("Courier", 10, "bold"), 
                                  relief="flat", width=2) # Botón de Ayuda (Transcendencia)
        self.btn_help.pack(side="left", padx=2) # Empaquetado Ayuda

        self.btn_reset = tk.Button(self.ctrl_frame, text="♻", command=self.reset_database_system, 
                                   bg="#0a0a0a", fg="#ff3366", font=("Courier", 10, "bold"), 
                                   relief="flat", width=2) # Botón de Reseteo (Aniquilación S3)
        self.btn_reset.pack(side="left", padx=2) # Empaquetado Reset
        
        self.btn_db_math = tk.Button(self.ctrl_frame, text="Σ SONIDO DE LA MATEMÁTICA", command=self.toggle_db_math_playback, 
                                     bg="#0a0a0a", fg="#d4af37", font=("Courier", 10, "bold"), relief="flat", padx=10) # Acceso a la base de datos armónica
        self.btn_db_math.pack(side="left", padx=10) # Empaquetado
        
        self.btn_zen = tk.Button(self.ctrl_frame, text="🧘 ZEN MEDITACIÓN", command=self.toggle_zen_meditation, 
                                     bg="#0a0a0a", fg="#ffffff", font=("Courier", 10, "bold"), relief="flat", padx=10) # Modo de resonancia bio-armónica
        self.btn_zen.pack(side="left", padx=10) # Empaquetado

        self.btn_motor = tk.Button(self.ctrl_frame, text="MOTOR: SÍ", command=self.toggle_motor,
                                   bg="#0a0a0a", fg="#00ffaa", font=("Courier", 10, "bold"), relief="flat", padx=10,
                                   width=11) # A/B: engine output or original stream
        self.btn_motor.pack(side="left", padx=10)

        self.btn_binaural = tk.Button(self.ctrl_frame, text="BINAURAL 7,83: NO", command=self.toggle_binaural,
                                      bg="#0a0a0a", fg="#777777", font=("Courier", 10, "bold"), relief="flat", padx=10,
                                      width=17) # Real binaural beat with headphones (200 Hz / 207.83 Hz)
        self.btn_binaural.pack(side="left", padx=10)

        self.subtitle_label = tk.Label( # Etiqueta informativa de convergencia
            self.header, text="SISTEMA DE CONVERGENCIA BIO-MATEMÁTICA | HEARTBEAT: 72 BPM", 
            bg="#010103", fg="#00ffcc", 
            font=("Courier", 10, "italic")
        )
        self.subtitle_label.pack() # Posicionamiento del subtítulo

        # --- SISTEMA DE PESTAÑAS (Simplificado: Solo Observatorio) ---
        self.notebook = ttk.Notebook(self.root) # Organizador de vistas
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5) # Posicionamiento del notebook

        # Configurar estilo para pestañas oscuras
        style = ttk.Style() # Gestor de estilos de ttk
        style.theme_use('default') # Uso del tema base
        style.configure("TNotebook", background="#010103", borderwidth=0) # Estilo del fondo
        style.configure("TNotebook.Tab", background="#0a0a0a", foreground="#777", padding=[10, 2], font=("Courier", 8)) # Estilo de la pestaña inactiva
        style.map("TNotebook.Tab", background=[("selected", "#1a1a1a")], foreground=[("selected", "#00ffaa")]) # Estilo de la pestaña activa

        self.tab_observatorio = tk.Frame(self.notebook, bg="#010103") # Pestaña del Observatorio
        self.notebook.add(self.tab_observatorio, text=" 💠 OBSERVATORIO ") # Inserción de la pestaña

        self.exegesis_label = tk.Label( # Texto explicativo de la transubstanciación
            self.tab_observatorio, 
            text="OBSERVATORIO DE TRANSUBSTANCIACIÓN: A diferencia de una radio convencional, este sistema decodifica las frecuencias armónicas de Mozart\n"
                 "para extraer en tiempo real los Ceros de Riemann (ρ) y el ADN de la Función Zeta, revelando la arquitectura matemática oculta en la belleza sonora.",
            bg="#010103", fg="#666666", 
            font=("Courier", 9),
            justify="center", pady=10
        )
        self.exegesis_label.pack() # Posicionamiento de la etiqueta

        # 2. FOOTER Y BARRA DE EXÉGESIS (Empaquetar al fondo primero)
        self.footer = tk.Frame(self.root, bg="#010103") # Marco inferior extremo
        self.footer.pack(fill="x", side="bottom", pady=5) # Posicionamiento
        self.status_var = tk.StringVar(value="[SISTEMA_OK] Aguardando flujo cuántico...") # Variable de estado dinámico
        self.status_label = tk.Label(self.footer, textvariable=self.status_var, bg="#010103", fg="#004433", font=("Courier", 8)) # Etiqueta de status técnico
        self.status_label.pack() # Empaquetado

        self.exegesis_bar = tk.Frame(self.root, bg="#0a0a0a", height=50, bd=1, relief="sunken") # Barra HUD de métricas cuánticas
        self.exegesis_bar.pack(fill="x", side="bottom", padx=10, pady=5) # Posicionamiento de la barra
        self.exegesis_bar.pack_propagate(False) # Bloqueo de re-dimensionamiento automático

        self.points_container = tk.Frame(self.exegesis_bar, bg="#0a0a0a") # Contenedor interno para los puntos de datos
        self.points_container.pack(expand=True) # Posicionamiento central

        self.point_vars = [tk.StringVar(value="---") for _ in range(4)] # Lista de variables para las métricas SSS
        colors = ["#00d4ff", "#ff3366", "#00ffaa", "#ffffff"] # Paleta de colores cuánticos
        titles = ["1.MODOS ENCENDIDOS", "2.ENERGÍA DE GRAVES (<120 Hz)", "3.SUMA DE GANANCIAS Gₙ", "4.VOLUMEN DE ENTRADA"] # Nombres de lo que mide cada indicador

        for i in range(4): # Bucle de creación de etiquetas de telemetría
            f = tk.Frame(self.points_container, bg="#0a0a0a") # Marco para cada punto
            f.pack(side="left", padx=50) # Posicionamiento horizontal
            tk.Label(f, text=titles[i], bg="#0a0a0a", fg="#777777", font=("Courier", 8, "bold")).pack() # Título de la dimensión
            tk.Label(f, textvariable=self.point_vars[i], bg="#0a0a0a", fg=colors[i], font=("Courier", 10, "bold")).pack() # Valor en tiempo real

        # 3. HUD DE ECUACIONES (Multi-línea para visualización total del cálculo)
        self.equation_hud_var = tk.StringVar() # Variable para la fórmula maestra dinámica
        self.equation_hud = tk.Label( # Visualizador HUD de la transubstanciación
            self.root, textvariable=self.equation_hud_var,
            bg="#010103", fg="#00ffaa", 
            font=("Courier", 14, "bold"),
            justify="center", bd=0, highlightthickness=0
        )
        self.equation_hud.pack(side="bottom", pady=5) # Posicionamiento del HUD central inferior

        # The notebook was packed first with expand=True and took all the height on screens
        # shorter than 1000 px, hiding the bottom bars. Re-pack it last so they keep their space.
        self.notebook.pack_forget()
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # 4. CONTENEDOR PRINCIPAL (En Pestaña Observatorio)
        self.main_container = tk.Frame(self.tab_observatorio, bg="#010103") # Marco para el flujo de datos principal
        self.main_container.pack(expand=True, fill="both", padx=20, pady=10) # Posicionamiento
        self.main_container.columnconfigure(0, weight=1) # Columna Azul (Knowledge Feed)
        self.main_container.columnconfigure(1, weight=2) # Columna Visual (Matplotlib)
        self.main_container.columnconfigure(2, weight=1) # Columna Rosa (DNA Feed)
        self.main_container.rowconfigure(0, weight=1) # Fila única expansible

        # Panel Izquierdo: Descubrimientos (Knowledge Feed)
        self.discovery_frame = tk.Frame(self.main_container, bg="#010103") # Marco para emanaciones
        self.discovery_frame.grid(row=0, column=0, sticky="nsew", padx=10) # Posicionamiento en grilla
        
        tk.Label(self.discovery_frame, text="EMANACIONES_DIVINAS", bg="#010103", fg="#00d4ff", font=("Courier", 10, "bold"), justify="center").pack(fill="x", pady=(0, 5)) # Título del panel azul
        self.discovery_feed = tk.Text( # Terminal de revelaciones
            self.discovery_frame, bg="#010103", fg="#00d4ff", 
            font=("Courier", 9, "italic"), bd=0, highlightthickness=0, state="disabled"
        )
        self.discovery_feed.pack(expand=True, fill="both") # Posicionamiento del feed de conocimiento

        # Panel Central: Visualizaciones
        self.viz_frame = tk.Frame(self.main_container, bg="#010103")
        self.viz_frame.grid(row=0, column=1, sticky="nsew")

        # Label de la Voz del Creador (Marquee)
        self.voice_var = tk.StringVar(value="SINTONIZANDO EL ESPÍRITU DE LA CREACIÓN...")
        self.voice_label = tk.Label(
            self.viz_frame, textvariable=self.voice_var,
            bg="#010103", fg="#ffffff", font=("Courier", 12, "bold")
        )
        self.voice_label.pack(pady=5)

        # Panel Derecho: Telemetría (DNA Feed)
        self.telemetry_frame = tk.Frame(self.main_container, bg="#010103")
        self.telemetry_frame.grid(row=0, column=2, sticky="nsew", padx=10)
        
        tk.Label(self.telemetry_frame, text="ADN DEL CREADOR (ρ)", bg="#010103", fg="#ff3366", font=("Courier", 10, "bold"), justify="center").pack(fill="x", pady=(0, 5))
        self.telemetry_feed = tk.Text(
            self.telemetry_frame, bg="#010103", fg="#ff3366", 
            font=("Courier", 9), bd=0, highlightthickness=0, state="disabled"
        )
        self.telemetry_feed.pack(expand=True, fill="both")

        # Dashboard de Visualización (Layout Centrado)
        if HAS_MATPLOTLIB:
            plt.style.use('dark_background')
            self.fig = plt.figure(figsize=(14, 8), facecolor='#010103')
            gs = self.fig.add_gridspec(1, 2, wspace=0.1) 
            
            # A. Orbe de Fourier (Izquierda)
            self.ax_orb = self.fig.add_subplot(gs[0, 0])
            self.ax_orb.set_facecolor('#010103')
            self.theta = np.linspace(0, 2*np.pi, self.chunk_size + 1)
            self.line_orb, = self.ax_orb.plot([], [], color='#00d4ff', lw=2, alpha=0.8)
            self.ax_orb.set_title("OBSERVATORIO_FOURIER", color="gray", loc="left", fontsize=10)
            self.ax_orb.axis('off')
            self.ax_orb.set_aspect('equal') # Same scale on both axes: the orb is a circle, not an oval
            
            # B. Bio-Pulse (Derecha) - Corazón dentro de Círculo
            self.ax_heart = self.fig.add_subplot(gs[0, 1])
            self.ax_heart.set_facecolor('#010103')
            self.heart_t = np.linspace(0, 2*np.pi, 1000)
            self.line_heart, = self.ax_heart.plot([], [], color='#ff3366', lw=4, zorder=10)
            self.line_heart_glow, = self.ax_heart.plot([], [], color='#ff3366', lw=10, alpha=0.2, zorder=9)
            self.line_orb_heart, = self.ax_heart.plot([], [], color='#00d4ff', lw=1.5, alpha=0.4, zorder=5)
            self.ax_heart.set_title("BIO_HEARTBEAT_SYNC", color="gray", loc="left", fontsize=10)
            self.ax_heart.axis('off')
            self.ax_heart.set_aspect('equal')

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
            self.canvas.get_tk_widget().pack(expand=True, fill="both")
        else:
            tk.Label(self.viz_frame, text="[VISUALES DESACTIVADOS]\nInstale python3-matplotlib para ver la convergencia.",
                     bg="#010103", fg="#555", font=("Courier", 12)).pack(expand=True)
        self.build_modes_panel()

        # Sistema de Emanaciones (Texto flotante)
        self.emanaciones = []
        
        # Inicializar el Diario de Riemann (Partitura Matemática)
        # Data folder: next to engine.py when it is writable (as before); otherwise, as in a
        # root-installed .deb, the user's ~/.local/share/radio-matematica-2
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        if os.access(self.script_dir, os.W_OK):
            self.data_dir = self.script_dir
        else:
            self.data_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "radio-matematica-2")
            os.makedirs(self.data_dir, exist_ok=True)
        # CSV diary in the data folder (not in the launch directory), appending between sessions
        log_path = os.path.join(self.data_dir, "diario_riemann_partitura.csv")
        new_log = not os.path.exists(log_path) or os.path.getsize(log_path) == 0
        self.log_file = open(log_path, "a", newline='')
        self.log_writer = csv.writer(self.log_file)
        if new_log:
            self.log_writer.writerow(["Timestamp", "Simbolo_Riemann", "Frecuencia_Hz", "Energia_Zeta"])
            self.log_file.flush()

        # 6. Base de Datos Maestro (SQLite)
        self.db_path = os.path.join(self.data_dir, "riemann_zenit.db")
        self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS registro_convergencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                simbolo TEXT,
                frecuencia_hz REAL,
                energia_zeta REAL,
                formula TEXT,
                hallazgo_infinito TEXT,
                titulo TEXT,
                artista TEXT
            )
        ''')
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS catalogo_canciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                artista TEXT,
                start_timestamp REAL,
                end_timestamp REAL,
                start_id INTEGER,
                end_id INTEGER
            )
        ''')
        self.db_conn.commit() # Consolidación de cambios en la base de datos
        
        # Verificar si las columnas existen (migración simple)
        for col in [("hallazgo_infinito", "TEXT"), ("titulo", "TEXT"), ("artista", "TEXT")]: # Lista de columnas necesarias
            try: # Intento de alteración de tabla
                self.db_cursor.execute(f"ALTER TABLE registro_convergencia ADD COLUMN {col[0]} {col[1]}") # Inyección de columna
                self.db_conn.commit() # Confirmación de migración
            except: # Captura de error si la columna ya existe
                pass # Continuar sin cambios

        # Añadir Menú Contextual para copia fácil
        self.setup_context_menus() # Inicialización de menús de interacción

    def setup_context_menus(self): # Configuración de menús emergentes globales
        """Configura un menú de clic derecho universal para copiar y pegar."""
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#111", fg="#00ffaa", activebackground="#00d4ff", activeforeground="#000") # Estilo del menú contextual
        self.context_menu.add_command(label="Cortar", command=lambda: self.active_widget.event_generate("<<Cut>>")) # Comando Cortar
        self.context_menu.add_command(label="Copiar", command=lambda: self.active_widget.event_generate("<<Copy>>")) # Comando Copiar
        self.context_menu.add_command(label="Pegar", command=lambda: self.active_widget.event_generate("<<Paste>>")) # Comando Pegar
        self.context_menu.add_separator() # Separador visual
        self.context_menu.add_command(label="Seleccionar Todo", command=self.select_all) # Comando Selección Total
        self.context_menu.add_command(label="Limpiar Panel", command=self.clear_panel) # Comando de limpieza de HUD

        # Vincular a todos los widgets de texto y entrada
        widgets_to_bind = [ # Lista de componentes que soportan el menú
            self.discovery_feed, self.telemetry_feed, self.equation_hud, 
            self.radio_search_entry
        ]
        for widget in widgets_to_bind: # Iteración de vinculación
            widget.bind("<Button-3>", self.show_context_menu) # Enlace al botón derecho del ratón
    
    def show_context_menu(self, event): # Activador visual del menú contextual
        self.active_widget = event.widget # Identificación del widget que recibió el clic
        self.context_menu.post(event.x_root, event.y_root) # Despliegue del menú en las coordenadas del ratón

    def select_all(self): # Implementación de la selección total de contenido
        if isinstance(self.active_widget, (tk.Entry, tk.Text)): # Verificación de tipo de widget
            if isinstance(self.active_widget, tk.Text): # Caso widget de texto multilínea
                self.active_widget.tag_add("sel", "1.0", "end") # Selección de todo el rango de texto
            else: # Caso widget de entrada de una línea
                self.active_widget.select_range(0, "end") # Selección de rango
                self.active_widget.icursor("end") # Posicionamiento del cursor al final

    def clear_panel(self): # Función de purgado de paneles de información
        if hasattr(self, 'active_widget'): # Verificación de existencia de widget activo
            state = self.active_widget.cget("state") # Captura del estado actual (bloqueado/desbloqueado)
            self.active_widget.config(state="normal") # Desbloqueo temporal para edición
            if isinstance(self.active_widget, tk.Text): # Caso texto
                self.active_widget.delete("1.0", "end") # Borrado total
            else: # Caso entrada
                self.active_widget.delete(0, "end") # Borrado total
            self.active_widget.config(state=state) # Restauración del estado original

    def play_audio(self): # Comando de activación del flujo sonoro
        """Reanuda o inicia el flujo de audio."""
        if self.playing_db_math: # Si se estaba reproduciendo matemática histórica
            self.playing_db_math = False # Detención del modo historia
            time.sleep(0.1) # Pausa técnica de conmutación
            
        if not self.audio_active: # Si el audio estaba apagado
            self.audio_active = True # Activación del flag de audio
            self.status_var.set("[SISTEMA] Reiniciando flujo...") # Notificación de reinicio
        self.paused = False # Desactivación del estado de pausa
        self.btn_play.config(fg="#ffffff") # Iluminación del botón Play
        self.btn_pause.config(fg="#00ffaa") # Atenuación del botón Pausa
        self.btn_db_math.config(fg="#d4af37", text="Σ SONIDO DE LA MATEMÁTICA") # Restauración de etiqueta

    def pause_audio(self): # Comando de suspensión temporal del audio
        """Pausa la salida de audio pero mantiene el proceso (silencio)."""
        self.paused = not self.paused # Conmutación del estado de pausa
        if self.paused: # Si se activa la pausa
            self.status_var.set("[SISTEMA] Audio en pausa (Análisis en curso)") # Notificación de silencio analítico
            self.btn_pause.config(fg="#ffffff") # Iluminación del botón Pausa
            self.btn_play.config(fg="#00ffaa") # Atenuación del botón Play
        else: # Si se desactiva la pausa
            self.status_var.set("[SISTEMA] Resonancia activa") # Notificación de resonancia recuperada
            self.btn_pause.config(fg="#00ffaa") # Atenuación Pausa
            self.btn_play.config(fg="#ffffff") # Iluminación Play

    def stop_audio(self): # Comando de aniquilación del flujo de audio
        """Detiene completamente los procesos de audio."""
        self.audio_active = False # Apagado del flag de audio
        self.playing_db_math = False # Apagado del flag de historia
        self.force_restart = True # Preparación para reinicio total
        self.status_var.set("[SISTEMA] Flujo detenido") # Notificación de parada total
        self.btn_play.config(fg="#00ffaa") # Reset de color
        self.btn_pause.config(fg="#00ffaa") # Reset de color
        self.btn_db_math.config(fg="#d4af37", text="Σ SONIDO DE LA MATEMÁTICA") # Reset de etiqueta
        if self.proc_in: self.proc_in.kill() # Terminación forzada del proceso de entrada
        if self.proc_out: self.proc_out.kill() # Terminación forzada del proceso de salida

    def show_help(self): # Despliegue de la base de conocimiento técnico
        """Muestra la explicación técnica de la modulación cuántico-matemática."""
        help_window = tk.Toplevel(self.root) # Creación de ventana secundaria
        help_window.title("📜 EL ARTE DE LA MODULACIÓN ZENIT") # Título de la ventana de ayuda
        help_window.geometry("700x500") # Dimensiones
        help_window.configure(bg="#050505") # Fondo oscuro
        
        msg = ( # Mensaje exegético sobre el funcionamiento del sistema
            "💠 ¿POR QUÉ SUENA TAN BIEN?\n\n"
            "Esta radio no es un reproductor pasivo. Es un MOLDEADOR MATEMÁTICO que aplica\n"
            "tres leyes físicas al flujo de audio en tiempo real:\n\n"
            "1. RECTIFICACIÓN DE RIEMANN: El motor busca los Ceros de Riemann (ρ) en la música.\n"
            "   Al alinear las frecuencias con la Línea Crítica (0.5), el caos sonoro se\n"
            "   limpia y se vuelve cristalino.\n\n"
            "2. RESONANCIA DE 432 HZ: Cuando el audio alcanza la 'Afinación de la Naturaleza',\n"
            "   el sistema entra en Convergencia Absoluta, eliminando el ruido computacional.\n\n"
            "3. BIO-SINCRONÍA (72 BPM): El flujo de datos se entrega al ritmo del corazón,\n"
            "   sincronizando el buffer de audio con el latido humano (1.2 Hz).\n\n"
            "EL RESULTADO: Una pureza sonora donde la matemática y el alma convergen."
        )
        
        tk.Label(help_window, text=msg, bg="#050505", fg="#00ffaa", 
                 font=("Courier", 10), justify="left", padx=20, pady=20).pack() # Etiqueta de contenido
        
        tk.Button(help_window, text="ENTENDIDO", command=help_window.destroy, 
                  bg="#1a1a1a", fg="#ffffff", relief="flat", padx=20).pack(pady=10) # Botón de cierre

    def reset_database_system(self): # Borra la base de datos y la crea de nuevo
        """Limpia la base de datos, reconecta y reinicia los registros."""
        from tkinter import messagebox # Importación local de diálogos de confirmación
        if not messagebox.askyesno("♻ RESET MAESTRO", "¿Deseas vaciar la tabla de datos y recrear la base de datos desde cero?\n\nEsta acción es irreversible."): # Confirmación de seguridad
            return # Abortar si el usuario no confirma

        try: # Bloque de ejecución de purga
            # 1. Cerrar conexión actual
            self.db_conn.close() # Cierre del descriptor de archivo de base de datos
            time.sleep(0.5) # Pausa para liberación de bloqueos de sistema operativo

            # 2. Borrar archivo físico si existe
            if os.path.exists(self.db_path): # Verificación de existencia física
                os.remove(self.db_path) # Eliminación del archivo del disco
            
            # 3. Reconectar y recrear tablas
            self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False) # Apertura de nueva base de datos limpia
            self.db_cursor = self.db_conn.cursor() # Obtención del cursor
            self.db_cursor.execute(''' # Reconstrucción de la estructura de telemetría
                CREATE TABLE IF NOT EXISTS registro_convergencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    simbolo TEXT,
                    frecuencia_hz REAL,
                    energia_zeta REAL,
                    formula TEXT,
                    hallazgo_infinito TEXT,
                    titulo TEXT,
                    artista TEXT
                )
            ''')
            self.db_cursor.execute(''' # Reconstrucción de la estructura del catálogo
                CREATE TABLE IF NOT EXISTS catalogo_canciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT,
                    artista TEXT,
                    start_timestamp REAL,
                    end_timestamp REAL,
                    start_id INTEGER,
                    end_id INTEGER
                )
            ''')
            self.db_conn.commit() # Confirmación de la nueva arquitectura

            # 4. Limpiar interfaces
            self.discovery_feed.configure(state="normal") # Desbloqueo de HUD azul
            self.discovery_feed.delete("1.0", tk.END) # Borrado de texto
            self.discovery_feed.configure(state="disabled") # Bloqueo

            self.telemetry_feed.configure(state="normal") # Desbloqueo de HUD rosa
            self.telemetry_feed.delete("1.0", tk.END) # Borrado de texto
            self.telemetry_feed.configure(state="disabled") # Bloqueo

            self.status_var.set("[SISTEMA_REINICIADO] Base de datos nueva y limpia.") # Notificación de éxito
            messagebox.showinfo("SUCESO", "La base de datos ha sido purificada y reconectada con éxito.") # Diálogo de confirmación

        except Exception as e: # Captura de fallos en el proceso de reseteo
            messagebox.showerror("ERROR", f"Fallo al resetear el sistema: {str(e)}") # Notificación de error

    def on_dial_interact(self, event): # Gestión de la interacción física con el dial de sintonía
        """Mueve la aguja y sintoniza dinámicamente si el movimiento es significativo."""
        x = event.x # Obtención de la coordenada X del ratón
        x = max(50, min(1750, x)) # Restricción del rango físico del dial
        
        # Actualizar visualmente
        self.dial_canvas.coords(self.dial_needle, x, 5, x, 45) # Reposicionamiento de la aguja roja
        self.dial_canvas.coords(self.dial_glow, x-5, 20, x+5, 30) # Reposicionamiento del resplandor
        
        freq = 88 + (x - 50) / 16.5 # Cálculo de la frecuencia de radio FM simulada
        self.status_var.set(f"[DIAL] Sintonía Dinámica: {freq:.1f} MHz") # Notificación en barra de status

        # Sintonía Automática al arrastrar (Debounce de 2 segundos y 100px)
        t_now = time.time() # Captura del tiempo actual
        if t_now - self.last_tune_time > 2.5 and abs(x - self.last_tune_x) > 150: # Lógica de filtrado de cambios bruscos
            self.last_tune_time = t_now # Actualización de marca temporal
            self.last_tune_x = x # Actualización de posición de referencia
            
            temas = ["Classical", "Mozart", "Opera", "Bach", "Baroque", "Chamber", "Symphony", "Piano"] # Lista de géneros por banda
            idx = int((x / 1800) * len(temas)) # Mapeo de posición a género
            tag = temas[max(0, min(len(temas)-1, idx))] # Selección del tag de búsqueda
            
            print(f"Auto-Sintonizando Banda: {tag} ({freq:.1f} MHz)...") # Log técnico
            self.radio_search_var.set(tag) # Actualización del campo de búsqueda
            
            # Realizar búsqueda y sintonizar la primera automáticamente
            def auto_tune(): # Hilo interno para sintonización sin bloqueo de UI
                try: # Bloque de red
                    url = f"https://de1.api.radio-browser.info/json/stations/byname/{tag}" # URL de la API de estaciones
                    req = urllib.request.Request(url, headers={'User-Agent': 'MozartZenit/1.0'}) # Creación de petición con agente
                    with urllib.request.urlopen(req) as response: # Ejecución de petición HTTP
                        data = json.loads(response.read().decode()) # Decodificación de JSON
                    if data: # Si hay resultados
                        data.sort(key=lambda x: x.get('votes', 0), reverse=True) # Ordenación por popularidad
                        best = data[0] # Selección de la mejor estación
                        self.root.after(0, lambda: self.apply_station_from_data(best)) # Aplicación en el hilo principal
                except: pass # Silenciar errores de conexión
            
            threading.Thread(target=auto_tune, daemon=True).start() # Lanzamiento del hilo de auto-sintonía

    def apply_station_from_data(self, station): # Ejecución del cambio de emisora
        """Aplica una emisora directamente desde el objeto de datos de la API."""
        name = station['name'] # Nombre de la estación
        url = station['url_resolved'] if station['url_resolved'] else station['url'] # Resolución de URL directa
        self.status_var.set(f"📻 SINTONIZADO: {name}") # Notificación visual
        self.stream_url = url # Actualización de la fuente de datos
        self.audio_active = True # Activación de flujo
        self.force_restart = True # Disparador de reinicio de pipeline
        
        # Limpieza agresiva para cambio rápido
        if self.proc_in: self.proc_in.kill() # Muerte instantánea del decodificador antiguo
        if self.proc_out: self.proc_out.kill() # Muerte instantánea del reproductor antiguo

    def on_dial_release(self, event): # Finalización del gesto de sintonía
        """Finaliza la sintonía."""
        self.status_var.set(f"[DIAL] Sintonía fijada.") # Confirmación de anclaje

    def perform_radio_search(self): # Buscador manual de emisoras en el éter global
        """Busca emisoras usando la API de Radio-Browser."""
        query = self.radio_search_var.get().strip() # Obtención del término de búsqueda purgado
        if not query: return # Abortar si la búsqueda está vacía
        
        self.status_var.set(f"[DIAL] Buscando '{query}' en el éter...") # Notificación de búsqueda
        
        def run_search(): # Hilo de búsqueda para evitar congelamiento de ventana
            try: # Bloque de red
                # API de Radio Browser (No requiere key)
                url = f"https://de1.api.radio-browser.info/json/stations/byname/{urllib.parse.quote(query)}" # URL codificada
                req = urllib.request.Request(url, headers={'User-Agent': 'MozartZenit/1.0'}) # Petición HTTP
                with urllib.request.urlopen(req) as response: # Ejecución
                    data = json.loads(response.read().decode()) # Lectura de resultados
                
                # Filtrar y ordenar por votos/clics para calidad
                data.sort(key=lambda x: x.get('votes', 0), reverse=True) # Calibración por consenso
                
                self.station_results = data[:100] # Almacenamiento de los 100 mejores candidatos
                names = [f"{s['name']} ({s['countrycode']}) [{s['codec']}]" for s in self.station_results] # Formateo de nombres
                
                self.root.after(0, lambda: self.update_radio_menu(names)) # Actualización de la interfaz
            except Exception as e: # Captura de fallos de red
                self.root.after(0, lambda: self.status_var.set(f"[DIAL] Error de búsqueda: {e}")) # Notificación de error

        threading.Thread(target=run_search, daemon=True).start() # Lanzamiento del hilo de búsqueda

    def update_radio_menu(self, names): # Refresco del menú desplegable de emisoras
        self.radio_results_menu['values'] = names # Actualización de lista de valores
        if names: # Si hay resultados
            self.radio_results_menu.set(names[0]) # Selección automática del primero
            self.status_var.set(f"[DIAL] Encontradas {len(names)} emisoras.") # Notificación de cantidad
        else: # Si no hay resultados
            self.status_var.set("[DIAL] No se encontraron emisoras.") # Notificación de vacío

    def on_radio_selected(self, event): # Gestión de la sintonía tras selección manual en menú
        """Maneja la selección de una emisora del buscador."""
        idx = self.radio_results_menu.current() # Obtención del índice seleccionado
        if idx < 0: return # Abortar si no hay selección válida
        
        station = self.station_results[idx] # Recuperación del objeto de datos de la estación
        name = station['name'] # Nombre de la emisora
        url = station['url_resolved'] if station['url_resolved'] else station['url'] # URL técnica
        
        print(f"Sintonizando: {name} -> {url}") # Log de sintonización
        print("DIAL", "CHANGE_STATION", f"{name} | {url}") # Log de auditoría
        
        self.stream_url = url # Actualización de URL maestra
        self.audio_active = True # Activación de audio
        self.force_restart = True # Petición de reinicio de procesos
        
        # Animar aguja del dial de forma determinista basada en el nombre
        pos = (hash(name) % 1700) + 50 # Cálculo de posición pseudo-aleatoria consistente
        self.dial_canvas.coords(self.dial_needle, pos, 5, pos, 45) # Movimiento de la aguja
        self.dial_canvas.coords(self.dial_glow, pos-5, 20, pos+5, 30) # Movimiento del brillo
        
        # Terminar procesos actuales de forma agresiva
        def kill_procs(): # Hilo de limpieza de procesos zombies
            try: # Bloque de terminación
                if self.proc_in: self.proc_in.terminate() # Señal de terminación 1
                if self.proc_out: self.proc_out.terminate() # Señal de terminación 1
                time.sleep(0.2) # Breve espera para liberación de memoria
                if self.proc_in: self.proc_in.kill() # Señal de aniquilación definitiva
                if self.proc_out: self.proc_out.kill() # Señal de aniquilación definitiva
            except: pass # Silenciar fallos si los procesos ya murieron
        
        threading.Thread(target=kill_procs, daemon=True).start() # Lanzamiento de limpieza

    def change_station(self, selection): # Comando directo de cambio de estación pre-configurada
        """Cambia la URL del stream y reinicia el proceso de audio."""
        self.stream_url = self.stations[selection] # Selección de URL del diccionario base
        self.status_var.set(f"[SISTEMA] Sincronizando: {selection}...") # Notificación de cambio
        self.audio_active = True # Asegurar audio activo
        self.force_restart = True # Reiniciar flujo
        
        # Terminar procesos actuales de forma agresiva
        if self.proc_in: # Si existe proceso de entrada
            try: self.proc_in.kill() # Aniquilación inmediata
            except: pass # Silenciar
        if self.proc_out: # Si existe proceso de salida
            try: self.proc_out.kill() # Aniquilación inmediata
            except: pass # Silenciar

    def toggle_db_math_playback(self): # Selector de modo: Radio en vivo vs Matemática histórica
        """Inicia o detiene la audición de la matemática histórica con parada de seguridad."""
        if not self.playing_db_math: # Si el modo historia está desactivado
            # 1. PARADA TOTAL DE RADIO
            self.playing_db_math = True # Activación de modo historia
            self.audio_active = False  # Desactivación de flujo de radio vivo
            self.status_var.set("[SISTEMA] Deteniendo radio y procesos de escritura...") # Notificación de transición
            
            # Matar procesos de radio para liberar aplay (PipeWire)
            if self.proc_in: self.proc_in.terminate() # Suspensión decodificador
            if self.proc_out: self.proc_out.terminate() # Suspensión reproductor
            time.sleep(0.5) # Esperar a que el sistema libere el hardware de audio (Hardware SSS Lock)
            
            self.btn_db_math.config(fg="#ff0000", text="⏹ DETENER MATEMÁTICA") # Cambio visual del botón a rojo
            threading.Thread(target=self.stream_db_math_audio, daemon=True).start() # Lanzamiento de síntesis histórica
        else: # Si el modo historia está activo
            self.playing_db_math = False # Desactivación de modo historia
            self.btn_db_math.config(fg="#d4af37", text="Σ SONIDO DE LA MATEMÁTICA") # Restauración visual
            self.status_var.set("[SISTEMA] Reiniciando flujo de radio...") # Notificación de regreso al vivo
            self.audio_active = True # Reactivación de flag de audio
            self.force_restart = True # Forzar reconstrucción de tubería de radio

    def stream_db_math_audio(self): # Motor de síntesis sonora de registros históricos Riemann
        """Sintetiza la base de datos con cursor independiente y prioridad de hardware."""
        try: # Bloque de procesamiento de base de datos
            # Conexión local para evitar errores de hilos (sqlite3 requiere esto)
            db_local = sqlite3.connect(self.db_path) # Conexión a la base de datos de la radio
            cursor_local = db_local.cursor() # Cursor local para aislamiento de hilos
            
            self.proc_out = subprocess.Popen( # Apertura del canal de salida PipeWire
                ['pw-play', '-a', '--rate', str(self.sample_rate), '--format', 's16', '--channels', '1', '-'], 
                stdin=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            
            cursor_local.execute("SELECT frecuencia_hz, energia_zeta, simbolo, titulo, artista FROM registro_convergencia ORDER BY id ASC LIMIT 6000") # Consulta de hallazgos
            
            duration = 0.3 # Duración de cada "gota" sonora matemática
            t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False) # Eje temporal de la gota
            fade = np.exp(-3 * t / duration) # Envolvente de caída exponencial
            
            count = 0 # Contador de notas procesadas
            while self.playing_db_math: # Bucle de síntesis infinita
                row = cursor_local.fetchone()
                if not row: break
                
                freq, energy, simbolo, titulo, artista = row
                if freq <= 0: freq = 432.0
                
                amp = np.clip(energy / 100.0, 0.01, 0.8)
                wave = amp * np.sin(2 * np.pi * freq * t) # Onda pura sin armónicos de abejorro
                
                audio_segment = (wave * fade * 32767).astype(np.int16)
                
                try:
                    self.proc_out.stdin.write(audio_segment.tobytes())
                    if count % 10 == 0: self.proc_out.stdin.flush()
                except: break
                
                count += 1
                if count % 20 == 0:
                    self.status_var.set(f"💠 AUDICIÓN PURA: {count}/6000 | F:{freq:.1f}Hz")
                
            db_local.close()
            self.playing_db_math = False
            self.root.after(0, lambda: self.btn_db_math.config(fg="#d4af37", text="Σ SONIDO DE LA MATEMÁTICA"))
            self.audio_active = True 
            
        except Exception as e:
            print(f"Error en flujo maestro: {e}")
            self.playing_db_math = False

    def build_modes_panel(self):
        """Live bars with the gain Gₙ of the 20 Riemann modes (left channel)."""
        self.modes_height = 110
        self.modes_canvas = tk.Canvas(self.viz_frame, height=self.modes_height, bg="#010103", highlightthickness=0)
        if HAS_MATPLOTLIB:
            self.modes_canvas.pack(side="bottom", fill="x", pady=(0, 4), before=self.canvas.get_tk_widget())
        else:
            self.modes_canvas.pack(side="bottom", fill="x", pady=(0, 4))
        self.modes_title = self.modes_canvas.create_text(10, 10, anchor="w", text="MODOS DE RIEMANN",
                                                         fill="#d4af37", font=("Courier", 9, "bold"))
        self.mode_bars, self.mode_texts = [], []
        for f in self.motor.update_f_peaks(self.sample_rate):
            label = f"{f:.0f}" if f < 1000 else f"{f / 1000:.1f}k"
            self.mode_bars.append(self.modes_canvas.create_rectangle(0, 0, 0, 0, fill="#1f3a4a", outline=""))
            self.mode_texts.append(self.modes_canvas.create_text(0, 0, text=label, fill="#777", font=("Courier", 7)))

    def update_modes_panel(self, freq_dom):
        width = max(self.modes_canvas.winfo_width(), 200)
        top, bottom = 24, self.modes_height - 16
        gains = self.motor.channels[0].mode_gains
        slot = (width - 20) / len(gains)
        for i, g in enumerate(gains):
            x0 = 10 + i * slot + slot * 0.18
            x1 = 10 + (i + 1) * slot - slot * 0.18
            y0 = bottom - (bottom - top) * min(float(g), 1.5) / 1.5
            self.modes_canvas.coords(self.mode_bars[i], x0, y0, x1, bottom)
            self.modes_canvas.itemconfig(self.mode_bars[i], fill="#00ffaa" if g > 0.1 else "#1f3a4a")
            self.modes_canvas.coords(self.mode_texts[i], (x0 + x1) / 2, bottom + 8)
        active = int(np.sum(gains > 0.1))
        motor = "SÍ" if self.motor_enabled else "NO (sonido original)"
        self.modes_canvas.itemconfig(
            self.modes_title,
            text=f"MODOS DE RIEMANN (Gₙ, canal izq.)  ·  activos {active}/20  ·  "
                 f"frecuencia dominante {freq_dom:.0f} Hz  ·  motor: {motor}")

    def update_indicators(self, estado):
        """Bottom bar: four values, each named after what it really measures."""
        gains = self.motor.channels[0].mode_gains
        rms = float(np.sqrt(np.mean(self.audio_data ** 2)))
        self.point_vars[0].set(f"{int(np.sum(gains > 0.1))}/{len(gains)}")
        self.point_vars[1].set(f"{estado.get('gamma_resonance', 0.0):.2f}")
        self.point_vars[2].set(f"{estado.get('zeta_energy', 0.0):.1f} / {1.5 * len(gains):.0f}")
        self.point_vars[3].set(f"{20 * np.log10(rms + 1e-9):.1f} dBFS" if rms > 1e-6 else "silencio")

    def add_binaural(self, block):
        """Adds carrier (left) and carrier + beat (right) to a (n, 2) block, phase-continuous."""
        out = np.array(block, dtype=np.float32, copy=True)
        n = len(out)
        for ch, f in enumerate((self.binaural_carrier_hz, self.binaural_carrier_hz + self.binaural_beat_hz)):
            step = 2 * np.pi * f / self.sample_rate
            phase = self.binaural_phase[ch] + step * np.arange(n)
            out[:, ch] += self.binaural_level * np.sin(phase)
            self.binaural_phase[ch] = float((self.binaural_phase[ch] + step * n) % (2 * np.pi))
        return out

    def toggle_binaural(self):
        self.binaural_enabled = not self.binaural_enabled
        if self.binaural_enabled:
            self.btn_binaural.config(text="BINAURAL 7,83: SÍ", fg="#d4af37")
        else:
            self.btn_binaural.config(text="BINAURAL 7,83: NO", fg="#777777")

    def toggle_motor(self):
        """Switches between hearing the engine and hearing the original stream."""
        self.motor_enabled = not self.motor_enabled
        if self.motor_enabled:
            self.btn_motor.config(text="MOTOR: SÍ", fg="#00ffaa")
            self.status_var.set("[MOTOR] Activado: suena la emisora pasada por el motor de Riemann.")
        else:
            self.btn_motor.config(text="MOTOR: NO", fg="#ff3366")
            self.status_var.set("[MOTOR] Desactivado: suena la emisora original, sin procesar.")

    def toggle_zen_meditation(self):
        """Inicia o detiene la meditación Zen pura (432Hz)."""
        if not self.playing_zen:
            self.playing_zen = True
            self.audio_active = False
            self.status_var.set("[SISTEMA] Iniciando Meditación Zen (432Hz)...")
            if self.proc_in: self.proc_in.terminate()
            if self.proc_out: self.proc_out.terminate()
            time.sleep(0.5)
            self.btn_zen.config(fg="#00ffaa", text="⏹ DETENER ZEN")
            threading.Thread(target=self.stream_zen_audio, daemon=True).start()
        else:
            self.playing_zen = False # Desactiva el estado de meditación.
            self.btn_zen.config(fg="#ffffff", text="🧘 ZEN MEDITACIÓN") # Restaura el estilo del botón.
            self.status_var.set("[SISTEMA] Finalizando meditación...") # Informa del fin de la sesión Zen.
            self.audio_active = True # Reactiva el flujo de audio estándar.

    def stream_zen_audio(self):
        """Sintetiza una onda pura de 432Hz para meditación sin ruido."""
        try:
            self.proc_out = subprocess.Popen( # Abre el canal hacia PipeWire para la onda pura.
                ['pw-play', '-a', '--rate', str(self.sample_rate), '--format', 's16', '--channels', '1', '-'], 
                stdin=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            duration = 1.0 # Segmento de 1 segundo para la síntesis.
            t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False) # Eje temporal.
            wave = 0.4 * np.sin(2 * np.pi * 432 * t) # Generación de la frecuencia de resonancia biológica.
            audio_segment = (wave * 32767).astype(np.int16) # Conversión a formato de audio crudo (PCM16).
            while self.playing_zen: # Bucle de persistencia de la onda Zen.
                try:
                    if self.proc_out.poll() is not None: break # Si el proceso muere, sale.
                    self.proc_out.stdin.write(audio_segment.tobytes()) # Inyecta la frecuencia en el hardware.
                    self.proc_out.stdin.flush() # Vacía el buffer para evitar latencia.
                except: break
                time.sleep(duration - 0.05) # Sincronización temporal del bucle.
            if self.proc_out: self.proc_out.terminate() # Cierre del proceso al finalizar.
        except Exception as e:
            print(f"Error Zen: {e}")
            self.playing_zen = False

    def update_song_catalog(self, t_now):
        """Opens a catalogo_canciones row when the song changes and closes the previous one."""
        full_ident = f"{self.current_artist}|{self.current_song}"
        if full_ident != self.last_recorded_song and self.current_song != "SINTONIZANDO": # Si cambia la canción...
            if self.current_song_start_id: # Cierra el registro de la canción anterior.
                self.db_cursor.execute("UPDATE catalogo_canciones SET end_timestamp = ? WHERE id = ?", (t_now, self.current_song_start_id))
            self.db_cursor.execute("INSERT INTO catalogo_canciones (titulo, artista, start_timestamp) VALUES (?, ?, ?)", (self.current_song, self.current_artist, t_now)) # Registra la nueva.
            self.last_recorded_song = full_ident
            self.current_song_start_id = self.db_cursor.lastrowid

    def update_math_engine(self):
        """[MAESTRO] Centralización de Indicadores y Persistencia Única."""
        if not self.audio_active or self.paused: return # Solo opera si hay flujo de datos.
        
        estado = self.motor.estado # Extrae el estado actual del motor matemático.
        t_now = time.time() # Marca temporal de la captura.
        
        # 1. Indicadores HUD y Exégesis (Tiempo Real)
        self.equation_hud_var.set(estado.get("formula_activa", "")) # Muestra la fórmula que rige el momento.
        pulse = estado.get("bio_pulse", 1.0) # Obtiene el pulso biológico de la señal.
        
        # Calcular FFT una sola vez para toda la telemetría
        fft_data = np.abs(np.fft.rfft(self.audio_data)) # Transformada rápida de Fourier para análisis espectral.
        freq_dom = np.argmax(fft_data) * (self.sample_rate / self.chunk_size) # Frecuencia dominante.
        z_energy = float(estado.get('zeta_energy', 0)) # Energía extraída de la función Zeta.
        
        self.update_indicators(estado)

        # 2. Persistencia Única en DB (Cada 5 frames de motor para estabilidad)
        try:
            simbolo = np.random.choice(estado.get("terminos_reales", ["ζ(s)"])) # Selecciona el símbolo matemático dominante.
            hallazgo = estado.get("alarma_infinito") # Detecta si se ha cruzado el umbral del infinito.
            
            self.db_cursor.execute( # Registra la exégesis en la base de datos para la posteridad.
                "INSERT INTO registro_convergencia (timestamp, simbolo, frecuencia_hz, energia_zeta, formula, hallazgo_infinito, titulo, artista) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (t_now, simbolo, float(freq_dom), z_energy, estado['formula_activa'], hallazgo, self.current_song, self.current_artist)
            )
            
            self.update_song_catalog(t_now) # Catálogo de canciones

            if int(t_now) % 10 == 0: self.db_conn.commit() # Commit espaciado para proteger el hardware.
            if hallazgo: self.trigger_alarma_visual(hallazgo) # Si hay hallazgo, activa la alarma de Jacobo.
        except Exception as e: # Report the first failure instead of hiding it
            if not getattr(self, "_db_error_reported", False):
                print(f"[BASE DE DATOS] No se pudo guardar el registro: {e}")
                self._db_error_reported = True
        
        # 3. Telemetría y Descubrimientos (UI)
        self.telemetry_feed.configure(state="normal")
        self.telemetry_feed.insert("1.0", f"[{time.strftime('%H:%M:%S')}] {simbolo:7} | Z:{z_energy:5.1f}\n") # Inyecta el símbolo en el feed.
        self.telemetry_feed.delete("20.0", "end")
        self.telemetry_feed.config(state="disabled")
        
        if z_energy > 200: # Si la energía Zeta supera el umbral crítico de clímax.
            self.discovery_feed.configure(state="normal")
            self.discovery_feed.insert("1.0", f"[{time.strftime('%H:%M:%S')}] >> CLÍMAX DETECTADO <<\n")
            self.discovery_feed.delete("15.0", "end")
            self.discovery_feed.config(state="disabled")

    def process_audio_stream(self):
        """Captura audio vía ffmpeg y reproduce vía aplay en un bucle persistente."""
        while self.running: # Bucle de vida del proceso de audio.
            if not self.audio_active: # Si está en modo Zen u otro, espera.
                time.sleep(0.5)
                continue

            self.force_restart = False
            self.status_var.set(f"[SISTEMA] Conectando a: {self.stream_url[:40]}...")
            
            # Comando FFMPEG con mejores headers y reconexión (CAMBIO A ESTÉREO PARA BINAURAL S3)
            cmd_in = [ # Configuración del receptor de flujo cuántico.
                'ffmpeg', 
                '-headers', 'User-Agent: MozartZenit/1.0 (X11; Linux x86_64) AppleWebKit/537.36\r\nIcy-MetaData: 1\r\n',
                '-reconnect', '1', '-reconnect_streamed', '1', '-reconnect_delay_max', '5',
                '-i', self.stream_url, 
                '-f', 's16le', '-ac', '2', '-ar', str(self.sample_rate), '-'
            ]
            
            try:
                self.proc_in = subprocess.Popen(cmd_in, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
                
                # Monitor de errores y metadatos
                def monitor_ffmpeg(proc): # Hilo secundario para extraer la exégesis de los metadatos.
                    import re
                    for line in proc.stderr:
                        try:
                            line_str = line.decode('utf-8', errors='ignore')
                            if "StreamTitle" in line_str or "Stream Title" in line_str: # Captura de título de canción.
                                match = re.search(r"Stream\s*Title\s*:\s*(.*)", line_str)
                                if match:
                                    full_title = match.group(1).strip().upper()
                                    self.status_var.set(f"🎵 {full_title}")
                                    
                                    # Descomponer en Artista y Canción
                                    if " - " in full_title: # Estructura estándar Artista - Título.
                                        partes = full_title.split(" - ", 1)
                                        self.current_artist = partes[0].strip()
                                        self.current_song = partes[1].strip()
                                    else:
                                        self.current_artist = "RADIO_SUIZA"
                                        self.current_song = full_title
                            elif "404" in line_str or "refused" in line_str or "403" in line_str:
                                print(f"Error Conexión: {line_str.strip()[:60]}")
                        except: pass

                threading.Thread(target=monitor_ffmpeg, args=(self.proc_in,), daemon=True).start()
                
                try:
                    # Asegurar que los procesos previos se cierren correctamente
                    if self.proc_out: # Limpieza de tuberías antes de nueva conexión.
                        try:
                            self.proc_out.stdin.close()
                            self.proc_out.terminate()
                            self.proc_out.wait(timeout=0.5)
                        except: pass
                    
                    self.proc_out = subprocess.Popen( # Inicia la salida física hacia los altavoces: ESTÉREO
                        ['pw-play', '-a', '--rate', str(self.sample_rate), '--format', 's16', '--channels', '2', '-'], 
                        stdin=subprocess.PIPE, stderr=subprocess.DEVNULL
                    )
                except Exception as e:
                    print(f"Error al iniciar aplay: {e}")
                    self.proc_out = None
                
                while self.running and not self.force_restart and self.audio_active: # Bucle de procesamiento.
                    # Lectura del flujo Estéreo (2 canales * 2 bytes = 4 bytes por frame)
                    raw = self.proc_in.stdout.read(self.chunk_size * 4) 
                    if not raw or self.force_restart: break # Si se corta el flujo, reinicia.
                    
                    # 1. Decodificación a Coma Flotante Estéreo
                    audio_int16 = np.frombuffer(raw, dtype=np.int16)
                    # Reshape forzado (N, 2) para separar canales
                    audio_radio = audio_int16.reshape(-1, 2).astype(np.float32) / 32768.0 
                    
                    # Guardar versión Mono (mixdown) para visualización S1
                    self.audio_data = np.mean(audio_radio, axis=1)
                    
                    # 2. RECTIFICACIÓN DE RIEMANN SSS (Sometimiento Hardware Real-Time) WITH BINAURAL PROCESSING
                    audio_motor = self.motor.rectificar_riemann(audio_radio, fs=self.sample_rate)
                    # The engine always runs (visuals keep moving); the button only chooses what you hear
                    audio_final = audio_motor if self.motor_enabled else audio_radio
                    if self.binaural_enabled:
                        audio_final = self.add_binaural(audio_final)
                    
                    # 3. Recodificación y Salida Física (Encoder/Decoder) con Limitador
                    audio_final = np.clip(audio_final, -1.0, 1.0) # Protege los transductores de picos infinitos.
                    raw_final = (audio_final * 32767).astype(np.int16).tobytes() # Reempaquetado para PipeWire.

                    if self.proc_out and not self.paused:
                        try:
                            if self.proc_out.poll() is None:
                                self.proc_out.stdin.write(raw_final) # Entrega final al hardware.
                                self.proc_out.stdin.flush()
                            else:
                                raise BrokenPipeError
                        except (BrokenPipeError, BrokenPipeError):
                            print("Tubería de audio rota, intentando reconectar...")
                            self.force_restart = True
                            break
                        except Exception as e:
                            print(f"Error de salida audio: {e}")
                            break
                    
                    # 4. Telemetría Matemática (Estado de Convergencia)
                    estado = self.motor.procesar_sonido(audio_radio) # El motor extrae la verdad del sonido.
                        
            except Exception as e:
                print(f"Fallo en motor de audio: {e}")
            
            # Limpieza exhaustiva
            if self.proc_in: # Cierre de procesos de entrada.
                try: self.proc_in.terminate(); self.proc_in.kill(); self.proc_in.wait()
                except: pass
            if self.proc_out: # Cierre de procesos de salida.
                try: self.proc_out.terminate(); self.proc_out.kill(); self.proc_out.wait()
                except: pass
            
            if not self.running: break
            if self.force_restart: 
                print("Reinicio de sintonización OK.")
                continue
            time.sleep(1.0)

    def trigger_alarma_visual(self, tipo):
        """Dispara una alerta visual y sonora cuando se detecta el infinito."""
        self.alarma_activa = True # Activa el estado de alerta.
        self.flash_state = not self.flash_state # Alternancia para el parpadeo.
        color = "#ff0000" if self.flash_state else "#ffffff" # Rojo/Blanco.
        
        self.status_label.config(fg=color) # Aplica el color al label de estado.
        self.status_var.set(f"⚠️ ¡ALERTA DE CONVERGENCIA! {tipo} DETECTADO ⚠️") # Mensaje de advertencia.
        
        # Alerta Visual (Sin sonido)
        if self.flash_state:
            pass

        # Inyectar en el feed de descubrimientos con prioridad
        self.discovery_feed.config(state="normal")
        self.discovery_feed.insert("1.0", f"!!! [{time.strftime('%H:%M:%S')}] {tipo} ENCONTRADO EN EL TIEMPO !!!\n", "alarma") # Registro del hallazgo.
        self.discovery_feed.tag_config("alarma", foreground="#ff0000", font=("Courier", 10, "bold")) # Estilo de alerta.
        self.discovery_feed.config(state="disabled")

    def animate(self):
        def update(frame):
            # 🚀 OPTIMIZACIÓN: Solo procesar si la radio está activa y no pausada
            if not self.audio_active or self.paused:
                return self.line_orb, self.line_heart

            estado = self.motor.estado # Estado actual del motor.
            
            # 1. Update Orbe (Fourier) - OPTIMIZADO: Usar FFT del motor
            fft_norm = estado.get("fft_norm", np.zeros(self.chunk_size + 1)) # Espectro normalizado.
            self._fft_norm = fft_norm
            
            # Vibración de la aguja del dial - OPTIMIZADO: Menos frecuencia
            if frame % 3 == 0: # Simulación de interferencia analógica cuántica.
                intensity = np.mean(fft_norm)
                jitter = (np.random.rand() - 0.5) * intensity * 10
                self.dial_canvas.move(self.dial_needle, jitter, 0) # Mueve la aguja.
                self.dial_canvas.move(self.dial_glow, jitter, 0) # Mueve el brillo.
            
            # 1. Update Orbe Izquierdo (Fourier)
            fft_norm = estado.get("fft_norm", np.zeros(self.chunk_size + 1))
            r_orb = 4.0 + fft_norm * 2.5 # Radio dinámico basado en la energía espectral.
            self.line_orb.set_data(r_orb * np.cos(self.theta), r_orb * np.sin(self.theta)) # Geometría sagrada.
            self.ax_orb.set_xlim(-7, 7)
            self.ax_orb.set_ylim(-7, 7)

            # --- GESTIÓN DE EMANACIONES (Hacia el exterior) ---
            if np.max(fft_norm) > 0.3 and frame % 5 == 0: # Si hay pico de energía, emana un símbolo.
                idx_pico = np.argmax(fft_norm)
                angle = self.theta[idx_pico]
                dist = r_orb[idx_pico]
                simbolo = np.random.choice(estado.get("terminos_reales", ["ζ(s)"]))
                txt = self.ax_orb.text(dist * np.cos(angle), dist * np.sin(angle), simbolo, color="#00ffaa", fontsize=11, alpha=0.9, fontweight='bold')
                self.emanaciones.append({"obj": txt, "vx": np.cos(angle)*0.15, "vy": np.sin(angle)*0.15, "life": 1.2}) # Física de la emanación.

            for em in self.emanaciones[:]: # Actualiza la posición de los símbolos flotantes.
                x, y = em["obj"].get_position()
                em["obj"].set_position((x + em["vx"], y + em["vy"]))
                em["life"] -= 0.04 # Decaimiento de la emanación.
                em["obj"].set_alpha(np.clip(em["life"], 0, 1))
                if em["life"] <= 0: # Si muere, se elimina del plano.
                    em["obj"].remove()
                    self.emanaciones.remove(em)

            # 2. Update Corazón Derecho (Bio-Pulse dentro de Círculo)
            pulse = estado.get("bio_pulse", 1.0)
            heart_scale = 1.0 + 0.2 * (pulse - 1.0) # Escalado del corazón por el pulso biológico.
            x_h = 16 * np.sin(self.heart_t)**3 # Ecuación paramétrica del corazón.
            y_h = 13 * np.cos(self.heart_t) - 5 * np.cos(2*self.heart_t) - 2 * np.cos(3*self.heart_t) - np.cos(4*self.heart_t)
            self.line_heart.set_data(x_h * heart_scale, y_h * heart_scale)
            self.line_heart_glow.set_data(x_h * heart_scale * 1.1, y_h * heart_scale * 1.1)
            
            # Orbe protector del corazón (AESTHETIC)
            r_protect = 18.0 + fft_norm * 2.0 # Campo de fuerza espectral.
            self.line_orb_heart.set_data(r_protect * np.cos(self.theta), r_protect * np.sin(self.theta))
            
            self.ax_heart.set_xlim(-25, 25)
            self.ax_heart.set_ylim(-25, 25)

            # --- CÁLCULOS VISUALES EN TIEMPO REAL ---
            self.equation_hud_var.set(estado["formula_activa"]) # HUD dinámico.
            
            # Actualizar barra de exégesis cada frame para fluidez total
            freq_dom = np.argmax(fft_norm) * (self.sample_rate / self.motor.N) # fft_norm comes from the motor's N-point FFT (4096), not from chunk_size
            self.update_modes_panel(freq_dom)
            self.update_indicators(estado)

            # Update Status y Telemetría - Cada 10 frames para no saturar UI pero mantener rastro
            if frame % 10 == 0:
                self.status_var.set(f"[MOZART_ZENIT] {self.motor.obtener_log()} | PULSE: {pulse:.2f}")
                
                # LA VOZ DEL CREADOR
                if frame % 150 == 0: # Revelaciones periódicas de Jacobo.
                    self.voice_var.set(np.random.choice(self.revelaciones))

                # --- TELEMETRÍA Y DESCUBRIMIENTOS (Ticker) ---
                simbolo = np.random.choice(estado.get("terminos_reales", ["ζ(s)"]))
                
                # ADN DEL CREADOR (Panel Derecho)
                self.telemetry_feed.config(state="normal")
                self.telemetry_feed.insert("1.0", f"[{time.strftime('%H:%M:%S')}] {simbolo:7} | Z:{estado['zeta_energy']:5.1f} | F:{freq_dom:7.1f}Hz\n") # Inyecta datos en el panel de telemetría.
                self.telemetry_feed.delete("25.0", "end")
                self.telemetry_feed.config(state="disabled")

                # EMANACIONES DIVINAS (Panel Izquierdo)
                desc = ""
                if estado["zeta_energy"] > 30: desc = f">> RESONANCIA: Sintonía en {simbolo}\n"
                if "ρ" in simbolo: desc = f">> LLAVE CUÁNTICA: Cero de Riemann detectado\n" # Identificación de singularidad matemática.
                
                if desc: # Si hay resonancia, se notifica en el feed de descubrimientos.
                    self.discovery_feed.config(state="normal")
                    self.discovery_feed.insert("1.0", f"[{time.strftime('%H:%M:%S')}] {desc}")
                    self.discovery_feed.delete("20.0", "end")
                    self.discovery_feed.config(state="disabled")

                # DIARIO CSV (independiente de la base de datos)
                try:
                    self.log_writer.writerow([f"{time.time():.3f}", simbolo, f"{freq_dom:.1f}", f"{estado['zeta_energy']:.3f}"])
                    if frame % 100 == 0: self.log_file.flush()
                except Exception as e:
                    if not getattr(self, "_csv_error_reported", False):
                        print(f"[DIARIO CSV] No se pudo escribir: {e}")
                        self._csv_error_reported = True

                # PERSISTENCIA EN BASE DE DATOS
                try: # Registro automático de la convergencia para análisis posterior.
                    self.db_cursor.execute(
                        "INSERT INTO registro_convergencia (timestamp, simbolo, frecuencia_hz, energia_zeta, formula, titulo, artista) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (time.time(), simbolo, float(freq_dom), float(estado['zeta_energy']), estado['formula_activa'], self.current_song, self.current_artist)
                    )
                    self.update_song_catalog(time.time())
                    if frame % 100 == 0: self.db_conn.commit()
                except Exception as e: # Report the first failure instead of hiding it (e.g. read-only database)
                    if not getattr(self, "_db_error_reported", False):
                        print(f"[BASE DE DATOS] No se pudo guardar el registro: {e}")
                        self._db_error_reported = True

            return [self.line_orb, self.line_heart, self.line_heart_glow, self.line_orb_heart] + [em["obj"] for em in self.emanaciones]

        # 🚀 OPTIMIZACIÓN: Bajar FPS a 20 (interval=50) para suavidad y ahorro
        self._fft_norm = np.zeros(self.chunk_size // 2)
        if HAS_MATPLOTLIB: # Inicia la animación de los orbes matemáticos.
            self.ani = FuncAnimation(self.fig, update, interval=50, blit=True, cache_frame_data=False)
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk() # Instancia principal de la interfaz gráfica.
    # Intentar fuente Orbitron si existe, si no, Courier
    app = MozartZenit(root) # Lanza la aplicación Mozart Zenit.
    
    def on_closing(): # Protocolo de apagado seguro del sistema.
        app.running = False # Detiene los bucles de audio.
        try:
            app.db_conn.commit() # Save pending rows (commits only happen every 100 frames)
            app.db_conn.close() # Cierra la conexión con la base de datos.
        except Exception as e:
            print(f"[BASE DE DATOS] Al cerrar: {e}")
        try:
            app.log_file.close() # Flush and close the CSV diary
        except Exception:
            pass
        root.destroy() # Destruye la ventana.
    
    root.protocol("WM_DELETE_WINDOW", on_closing) # Vincula el cierre de ventana con el apagado seguro.
    root.mainloop() # Inicia el ciclo de eventos de la UI.
