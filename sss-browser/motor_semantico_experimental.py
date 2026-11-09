# -*- coding: utf-8 -*-
import math
import numpy as np
from scipy.special import jv

# --- CONSTANTES DE LA FÓRMULA SSS ---
S1_BESSEL_STABILITY = -1.9041
S3_KP_ANNIHILATION = 1.832827

def calcular_resonancia_bessel(alpha, rho):
    """S1: Resonancia de Bessel para estabilidad entrópica."""
    x = alpha * rho
    return jv(1, x) * math.exp(S1_BESSEL_STABILITY)

def metrica_schwarzschild_logica(alpha, distancia_radial):
    """S2: Horizonte de Schwarzschild Lógico para curvatura del espacio."""
    rs = 2 * alpha
    denominador = 1 - (rs / max(distancia_radial, 1e-9))
    if denominador > 0:
        return 1.0 / math.sqrt(denominador)
    else:
        return 100.0 # Máxima atracción semántica

def derivada_sometimiento_kp(t):
    """S3: Aniquilación de Fase para eliminación de ruido."""
    kp = S3_KP_ANNIHILATION
    return (kp / 2.0) * (jv(0, kp * t) - jv(2, kp * t))

def transformar_alpha_experimental(alpha, rho, sigma):
    """INTEGRACIÓN FINAL SSS (Ecuación de Unificación de Jacobo Cánovas García)."""
    # Fase S1
    res_bessel = calcular_resonancia_bessel(alpha, rho)
    # Fase S2
    distancia = 1.0 / (sigma + 1e-9)
    grav_semantica = metrica_schwarzschild_logica(alpha, distancia)
    # Fase S3
    t = 1.0 - alpha
    anulacion_ruido = derivada_sometimiento_kp(t)
    
    # Unificación
    alpha_sss = alpha * (res_bessel + grav_semantica) * abs(anulacion_ruido)
    return max(0.0, alpha_sss)
