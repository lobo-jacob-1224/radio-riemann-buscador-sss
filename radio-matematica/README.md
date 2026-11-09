# Radio Matemática

**Versión 2.0.1** · Python · Linux

Radio por Internet que no se limita a reproducir. Cada bloque de audio de la emisora pasa por un **motor matemático** que coloca 20 filtros en frecuencias sacadas de los **ceros de la función zeta de Riemann**. Las ganancias de esos filtros siguen a la música en tiempo real. La ventana muestra el espectro, el estado de los 20 modos y lo que va midiendo el motor, y lo guarda todo en una base de datos.

---

## Qué hace

1. **Sintoniza** una emisora (hay 12 predefinidas de música clásica y jazz) o busca entre miles con la API pública de [Radio Browser](https://www.radio-browser.info/).
2. **Decodifica** el audio con `ffmpeg` a estéreo de 16 bits y 44 100 Hz.
3. **Procesa** cada bloque de 2048 muestras con el motor de Riemann (canal izquierdo y derecho por separado).
4. **Reproduce** el resultado con `pw-play` (PipeWire).
5. **Muestra** el orbe de Fourier, el corazón a 72 pulsaciones por minuto, las barras de los 20 modos y cuatro indicadores.
6. **Guarda** cada medida en SQLite (`riemann_zenit.db`) y en un diario CSV, junto al título y el artista que emite la radio.

## La matemática paso a paso

Todo está en [`motor_convergencia_infinito.py`](motor_convergencia_infinito.py), clase `MotorConvergencia`. En la radio se usa con `chunk_size = 4096`.

### 1. Los 20 ceros de Riemann

Los ceros no triviales de $\zeta(s)$ conocidos están todos en la recta crítica $\operatorname{Re}(s)=\tfrac12$, con la forma $\rho_n=\tfrac12+i\gamma_n$. El motor guarda los 20 primeros $\gamma_n$:

```
14.13472514  21.02203964  25.01085758  30.42487612  32.93506159
37.58617816  40.91871901  43.32707328  48.00515088  49.77383248
52.97032148  56.44624770  59.34704400  60.83177852  65.11254405
67.07981053  69.54640171  72.06715767  75.70469070  77.14484007
```

Son una **tabla fija**: el motor no los calcula a partir de la música. Lo que hacen es decidir **dónde** se colocan los 20 filtros.

### 2. De ceros a frecuencias: escala logarítmica

Cada $\gamma_n$ se normaliza entre 0 y 1 y se lleva a la banda audible con una escala exponencial. Así, la separación entre ceros se convierte en intervalos musicales y no en hercios fijos:

$$u_n=\frac{\gamma_n-\gamma_1}{\gamma_{20}-\gamma_1},\qquad f_n=f_{\min}\left(\frac{f_{\max}}{f_{\min}}\right)^{u_n}$$

con $f_{\min}=50$ Hz y $f_{\max}=\min(16000,\ f_s/2-1000)=16000$ Hz. El tope está en 16 kHz porque las emisoras MP3 no llevan nada por encima de unos 16,5 kHz. Las 20 frecuencias que salen son:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $f_n$ (Hz) | 50,0 | 93,9 | 135,3 | 222,1 | 279,5 | 427,9 | 580,6 | 723,8 | 1110,7 | 1305,9 |

| n | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| $f_n$ (Hz) | 1749,8 | 2405,4 | 3137,0 | 3593,7 | 5317,9 | 6367,3 | 7980,4 | 10051,8 | 14023,7 | 16000,0 |

### 3. Análisis: transformada de Fourier por ventanas (STFT)

- Ventana de Hann de $N=4096$ muestras, avance de $H=2048$ (solapamiento del 50 %).
- Cada bloque nuevo de 2048 muestras se une a las 2048 anteriores, se multiplica por la ventana y se calcula `rfft`.
- Resolución en frecuencia: $f_s/N = 44100/4096 \approx 10{,}77$ Hz por casilla.

### 4. Ganancias modales $G_n(t)$: seguidores de envolvente

Para cada modo se mide la energía cerca de su frecuencia, a ±12 Hz:

$$E_n=\operatorname{media}\{\,|X(f)| : |f-f_n|\le 12\text{ Hz}\,\},\qquad T_n=\operatorname{clip}(2E_n,\ 0,\ 1{,}5)$$

La ganancia persigue ese objetivo, rápido al subir y lento al bajar:

$$G_n\leftarrow G_n+c\,(T_n-G_n),\qquad c=\begin{cases}0{,}05 & T_n>G_n\ \text{(ataque)}\\ 0{,}002 & T_n\le G_n\ \text{(caída)}\end{cases}$$

Como se aplica una vez por bloque (cada $2048/44100\approx 46$ ms), la constante de tiempo es $\tau=-\Delta t/\ln(1-c)$: **unos 0,91 s al subir y unos 23 s al bajar**. Un modo "se enciende" cuando la música pasa por su banda y se queda sonando un buen rato después.

### 5. La máscara de Riemann

$$M(f)=0{,}6+\sum_{n=1}^{20}G_n\,\exp\!\left[-\frac12\left(\frac{f-f_n}{\sigma}\right)^2\right],\qquad \sigma=12\text{ Hz}$$

y se limita a $[0{,}1,\ 3]$. Fuera de los modos el espectro queda multiplicado por 0,6 (unos −4,4 dB). Dentro de un modo encendido puede llegar a ×2,1 (+6,4 dB) respecto al original. Es decir, **la máscara realza las 20 bandas de Riemann donde la música tiene energía**.

### 6. Fase con Bessel

Un acumulador de fase avanza $\theta\leftarrow\theta+2\pi H/f_s$ en cada bloque. A cada casilla de frecuencia se le suma la fase

$$\varphi(f)=\frac{\pi}{6}\,J_1(\theta \bmod 2\pi)\,\frac{f}{f_{\max}}$$

donde $J_1$ es la función de Bessel de primera especie y orden 1. Una fase proporcional a la frecuencia equivale a un **desplazamiento en el tiempo**. Como $|J_1|\le 0{,}582$, el desplazamiento máximo es de unos 2,2 µs (0,1 muestras), así que no cambia el timbre. El indicador **GRACIA** de la ventana vale $(1-|J_1(\theta)|)\cdot 100\,\%$.

### 7. Reconstrucción, calidez y suma solapada

$$Y(f)=X(f)\cdot M(f)\cdot e^{i\varphi(f)}\ \xrightarrow{\ \text{irfft}\ }\ y$$

**Saturación suave** con el volumen compensado:

$$y_w=\tanh(1{,}2\,y)\cdot\frac{\operatorname{RMS}(y)}{\operatorname{RMS}(\tanh(1{,}2\,y))}$$

**Suma solapada (OLA)** con compensación de ventana: cada trama se vuelve a multiplicar por la ventana $w$ y se acumula, junto con $w^2$. La salida es $\sum w\,y_w\,/\,\sum w^2$, lo que reconstruye la señal sin ondulaciones de volumen.

### 8. Estéreo

Los dos canales tienen su propio estado (búferes y ganancias). En el canal derecho los 20 modos se colocan **7,83 Hz más arriba**: $f_n^{R}=f_n+7{,}83$.

Aparte, el botón **BINAURAL 7,83** (apagado al arrancar) suma un pulso binaural real: 200 Hz en el oído izquierdo y 207,83 Hz en el derecho, a −30 dBFS y con fase continua entre bloques. Necesita auriculares.

### 9. Lo que se dibuja

- **Orbe de Fourier**: el espectro normalizado en coordenadas polares, $r(\theta)=4+2{,}5\,|X|_{\text{norm}}$.
- **Corazón**: la curva paramétrica $x=16\sin^3 t,\ y=13\cos t-5\cos 2t-2\cos 3t-\cos 4t$, escalada por un pulso de 1,2 Hz (72 latidos por minuto): $1+0{,}1\sin(2\pi\cdot 1{,}2\,t)$.
- **Barras de los 20 modos**: $G_n$ del canal izquierdo; se pintan en verde cuando $G_n>0{,}1$.

### 10. Los cuatro indicadores

| Indicador | Cálculo |
|---|---|
| Modos encendidos | número de $G_n>0{,}1$, sobre 20 |
| Energía de graves | $\ln(1+50\cdot\text{media de las 12 primeras casillas})$; las 12 primeras casillas van de 0 a unos 118 Hz |
| Suma de ganancias | $\sum G_n$, como máximo $1{,}5\times 20=30$ |
| Volumen de entrada | $20\log_{10}\operatorname{RMS}$ en dBFS |

## Modos de escucha

| Botón | Qué suena |
|---|---|
| **MOTOR: SÍ / NO** | La emisora pasada por el motor, o la emisora original (para comparar). El motor sigue calculando en los dos casos. |
| **BINAURAL 7,83** | Añade el pulso binaural de 200 / 207,83 Hz. |
| **Σ SONIDO DE LA MATEMÁTICA** | Para la radio y toca los registros guardados: cada fila es una nota de 0,3 s con la frecuencia dominante que se midió, volumen $\operatorname{clip}(E/100,\ 0{,}01,\ 0{,}8)$ y caída $e^{-3t/0{,}3}$. Hasta 6000 notas. |
| **ZEN MEDITACIÓN** | Un tono puro continuo de 432 Hz. |
| **♻** | Borra la base de datos y la crea de nuevo (pide confirmación). |

## Datos que guarda

Si la carpeta del programa admite escritura, los datos se guardan ahí. Si no (por ejemplo, instalado como paquete), van a `~/.local/share/radio-matematica-2/`.

- `riemann_zenit.db` (SQLite)
  - `registro_convergencia`: momento, símbolo, frecuencia dominante (Hz), $\sum G_n$, fórmula activa, título y artista.
  - `catalogo_canciones`: cada canción con su inicio y su final.
- `diario_riemann_partitura.csv`: momento, símbolo, frecuencia y $\sum G_n$.

El símbolo de cada registro ($\zeta(s)$, $\rho_n$, $\Gamma(s)$, $\pi(x)$, $\mathrm{Li}(x)$, $\psi(x)$, $\Sigma$, $\infty$) se elige al azar de esa lista. La frecuencia y la energía sí son medidas.

## Instalación

Debian, Ubuntu o derivadas:

```bash
sudo apt install python3 python3-tk python3-numpy python3-scipy python3-matplotlib ffmpeg pipewire-bin
```

O con pip:

```bash
pip install -r requirements.txt   # y ffmpeg + pw-play del sistema
```

## Uso

```bash
cd radio-matematica
python3 engine.py
```

Sin Matplotlib la radio sigue funcionando: suena y guarda datos, pero sin gráficos.

**Usar el motor en tu propio código:**

```python
import numpy as np
from motor_convergencia_infinito import MotorConvergencia

motor = MotorConvergencia(chunk_size=4096)        # N = 4096, avance 2048
bloque = np.zeros((2048, 2), dtype=np.float32)    # 2048 muestras estéreo en [-1, 1]
salida = motor.rectificar_riemann(bloque, fs=44100)
print(motor.channels[0].mode_gains)               # las 20 ganancias G_n
```

El bloque de entrada tiene que tener exactamente `chunk_size / 2` muestras.

## Arquitectura

```
emisora ──ffmpeg──► PCM s16 estéreo ──► MotorConvergencia ──► [binaural] ──► pw-play ──► altavoces
                                              │
                                              ├──► estado (G_n, espectro) ──► ventana Tk + Matplotlib (20 fps)
                                              └──► SQLite + CSV
```

- Un hilo lee y procesa el audio. La animación lee el estado del motor 20 veces por segundo.
- Los títulos de las canciones salen de los metadatos ICY de la emisora (`StreamTitle`).
- NumPy está limitado a un hilo para que el audio no se corte.

## Limitaciones conocidas

- `radio_cuantica.py` crea el motor con el `chunk_size` por defecto (1024) pero le pasa bloques de 2048 muestras. Con el motor actual falla con `ValueError: could not broadcast input array from shape (2048,) into shape (512,)`. El programa principal es `engine.py`.
- La salida de audio necesita PipeWire (`pw-play`).
- Algunas emisoras predefinidas pueden haber cambiado de dirección. El buscador encuentra alternativas.

## Paquete Debian

En `packaging/` están el lanzador (`/usr/bin/radio-matematica-2`), el acceso directo y el icono del paquete `radio-matematica-2_2.0.1-1_all.deb`.
