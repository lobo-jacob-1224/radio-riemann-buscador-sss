#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
🌀 MOTOR DE CONVERGENCIA INFINITO - RIGOR DSP SSS v44.0 🌀
================================================================================
Implementación REAL con ECUACIÓN MODAL y MÁSCARA DINÁMICA:
- Seguidores de Envolvente G_n(t) con Ataque/Decay por modo.
- Máscara Modal STFT reactiva a la energía del streaming.
- Normalización OLA (Overlap-Add) con compensación de ventana.
- Saturación Tanh con normalización RMS en el dominio del tiempo.
================================================================================
"""

import numpy as np
import scipy.special
import time

try:
    from scipy.signal.windows import hann
except ImportError:
    try:
        from scipy.signal import hann
    except ImportError:
        def hann(M): return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(M) / (M - 1))

class MotorConvergencia:
    def __init__(self, num_zeros=30, chunk_size=1024):
        print("[MOTOR DE RIEMANN] 20 modos, estéreo")
        
        self.N = chunk_size
        self.HOP = chunk_size // 2
        self.WINDOW = hann(self.N)
        
        # 2) Ceros de Riemann (Identidad de la Verdad)
        self.zeros_im = np.array([
            14.13472514, 21.02203964, 25.01085758, 30.42487612, 32.93506159,
            37.58617816, 40.91871901, 43.32707328, 48.00515088, 49.77383248,
            52.97032148, 56.44624770, 59.34704400, 60.83177852, 65.11254405,
            67.07981053, 69.54640171, 72.06715767, 75.70469070, 77.14484007
        ])
        
        self.N_modes = len(self.zeros_im)
        
        # 3) Estado de Ganancia Modal por Canal (Estéreo Independiente)
        class ChannelState:
            def __init__(self, N, n_modes):
                self.input_buffer = np.zeros(N)
                self.output_buffer = np.zeros(N)
                self.norm_buffer = np.zeros(N)
                self.mode_gains = np.zeros(n_modes)
                self.phase_acc = 0.0
        
        self.channels = [ChannelState(self.N, self.N_modes) for _ in range(2)] # [0]=L, [1]=R
        
        self.attack_coeff = 0.05 # applied once per block (HOP=2048 at 44.1 kHz): time constant ~0.93 s
        self.decay_coeff = 0.002 # applied once per block: time constant ~23 s

        self.t_start = time.time()
        
        self.estado = {
            "zeta_energy": 0.0,
            "gamma_resonance": 0.0,
            "prime_density": 0.0,
            "formula_activa": "Resonancia Modal Activa",
            "fft_norm": np.zeros(self.N // 2 + 1),
            "terminos_reales": ["ζ(s)", "ρ_n", "Γ(s)", "π(x)", "Li(x)", "ψ(x)", "Σ", "∞"]
        }

    def update_f_peaks(self, fs):
        """Mapeo Log-Warp de ceros a frecuencias audibles."""
        tn = self.zeros_im
        tn_norm = (tn - tn.min()) / (tn.max() - tn.min() + 1e-9)
        # Top mode capped at 16 kHz: MP3 radio streams carry nothing above ~16.5 kHz,
        # so modes placed higher (18.3 and 21.05 kHz before) never had anything to reinforce.
        f_min, f_max = 50.0, min(16000.0, fs/2.0 - 1000.0)
        return f_min * (f_max / f_min) ** tn_norm

    def _process_single_channel(self, audio_chunk, ch_idx, fs, freq_offset=0.0):
        """Procesa un canal individual con OLA y Máscara de Riemann."""
        ch = self.channels[ch_idx]
        
        # A. ENTRADA Y VENTANEO
        ch.input_buffer[:self.HOP] = ch.input_buffer[self.HOP:]
        ch.input_buffer[self.HOP:] = audio_chunk.astype(np.float32)
        frame = ch.input_buffer * self.WINDOW
        
        # B. ANÁLISIS ESPECTRAL
        fft_complex = np.fft.rfft(frame)
        freqs = np.fft.rfftfreq(self.N, 1.0/fs)
        magnitudes = np.abs(fft_complex)
        
        # C. ACTUALIZACIÓN DE GANANCIAS MODALES G_n(t)
        f_peaks = self.update_f_peaks(fs)
        # Aplicar desplazamiento binaural al mapa de frecuencias objetivo (solo para el canal derecho)
        f_peaks_target = f_peaks + freq_offset 
        
        sigma_hz = 12.0 # Ancho de banda de cada modo
        
        for i, fn in enumerate(f_peaks_target):
            # Analizar energía en la vecindad del modo
            band_idx = np.logical_and(freqs >= fn - sigma_hz, freqs <= fn + sigma_hz)
            band_energy = np.mean(magnitudes[band_idx]) if np.any(band_idx) else 0.0
            
            # Objetivo de ganancia basado en la presencia de señal
            target = np.clip(band_energy * 2.0, 0.0, 1.5)
            
            # Ataque y Decay exponencial
            if target > ch.mode_gains[i]:
                ch.mode_gains[i] += self.attack_coeff * (target - ch.mode_gains[i])
            else:
                ch.mode_gains[i] += self.decay_coeff * (target - ch.mode_gains[i])

        # D. CONSTRUCCIÓN DE MÁSCARA MODAL
        mask = np.ones_like(freqs, dtype=np.float32) * 0.6
        for i, fn in enumerate(f_peaks_target):
            # M(t,ω) = 1 + sum(G_n * exp(...))
            mask += ch.mode_gains[i] * np.exp(-0.5 * ((freqs - fn) / sigma_hz)**2)

        # E. FASE CAUSAL Y SINCRO BESSEL
        ch.phase_acc += (2 * np.pi * 1.0 * self.HOP / fs)
        bessel_idx = scipy.special.jv(1, float(ch.phase_acc % (2 * np.pi)))
        phi_per_bin = (bessel_idx * np.pi / 6.0) * (freqs / (freqs.max() + 1e-9))
        
        # Aplicación al espectro complejo
        fft_mod = fft_complex * np.clip(mask, 0.1, 3.0) * np.exp(1j * phi_per_bin)

        # F. RECONSTRUCCIÓN iSTFT
        frame_rect = np.fft.irfft(fft_mod, n=self.N)
        
        # G. NO LINEALIDAD (Warmth con Normalización RMS)
        pre_gain = 1.2
        y = np.tanh(pre_gain * frame_rect)
        rms_in = np.sqrt(np.mean(frame_rect**2) + 1e-12)
        rms_out = np.sqrt(np.mean(y**2) + 1e-12)
        frame_warm = y * (rms_in / rms_out)
        
        # H. OVERLAP-ADD CON COMPENSACIÓN DE VENTANA
        frame_final = frame_warm * self.WINDOW
        ch.output_buffer += frame_final
        ch.norm_buffer += self.WINDOW**2 
        
        out_chunk = ch.output_buffer[:self.HOP].copy()
        norms = ch.norm_buffer[:self.HOP].copy()
        norms[norms < 1e-6] = 1.0
        out_chunk /= norms
        
        # Desplazamiento
        ch.output_buffer[:self.HOP] = ch.output_buffer[self.HOP:]
        ch.output_buffer[self.HOP:] = 0
        ch.norm_buffer[:self.HOP] = ch.norm_buffer[self.HOP:]
        ch.norm_buffer[self.HOP:] = 0
        
        # Actualizar telemetría global (solo canal 0 o promedio)
        if ch_idx == 0:
            self.estado["zeta_energy"] = float(np.sum(ch.mode_gains))
            self.estado["fft_norm"] = magnitudes / (np.max(magnitudes) + 1e-9)
            self.estado["formula_activa"] = f"MODOS_ACTIVOS: {np.sum(ch.mode_gains > 0.1)} | GRACIA: {(1.0-np.abs(bessel_idx))*100:.1f}%"
            
        return out_chunk

    def rectificar_riemann(self, audio_chunk, fs=44100):
        # Determinar si es Mono o Estéreo
        if len(audio_chunk.shape) == 1:
            # Entrada Mono (1D)
            return self._process_single_channel(audio_chunk, 0, fs, freq_offset=0.0)
        else:
            # Entrada Estéreo (2D -> [samples, channels])
            left_in = audio_chunk[:, 0]
            right_in = audio_chunk[:, 1]
            
            # Procesar Canal Izquierdo (Base)
            left_out = self._process_single_channel(left_in, 0, fs, freq_offset=0.0)
            
            # Procesar Canal Derecho (Binaural Offset +7.83Hz Schumann)
            right_out = self._process_single_channel(right_in, 1, fs, freq_offset=7.83)
            
            # Recombinar
            return np.stack([left_out, right_out], axis=1).astype(np.float32)

    def procesar_sonido(self, audio_chunk, sample_rate=44100):
        low_f = np.mean(self.estado["fft_norm"][:12])
        self.estado["gamma_resonance"] = float(np.log1p(low_f * 50))
        
        # Densidad de Primos estimada por la energía de los ceros (Usando Canal L como referencia S1)
        self.estado["prime_density"] = float(np.sum(self.channels[0].mode_gains > 0.1) / (self.N_modes + 1e-6))
        
        t_rel = time.time() - self.t_start
        self.estado["bio_pulse"] = 1.0 + 0.1 * np.sin(2 * np.pi * 1.2 * t_rel)
        return self.estado

    def obtener_log(self):
        return f"Z_MODAL: {self.estado['zeta_energy']:.2f} | {self.estado['formula_activa']}"
