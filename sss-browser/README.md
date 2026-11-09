# SSS Browser

**Versión 2.0.5** · Python · Linux

Buscador web con ventana propia. Busca en Internet, mide con un modelo de lenguaje (**MiniLM**) cuánto se parece cada resultado a lo que has buscado y pasa esa medida por la **fórmula SSS**, que ordena los resultados y calcula el **punto de sincronía** $\alpha^*$. Si se abre en Google Chrome, **Gemini Nano** (el modelo que viene dentro de Chrome) puntúa también los resultados, esa puntuación se fusiona con MiniLM y Nano escribe un resumen con las fuentes citadas.

Todo se ejecuta en tu ordenador: el servidor escucha solo en `127.0.0.1`, MiniLM funciona en el procesador y Gemini Nano funciona dentro de Chrome.

---

## Qué hace

1. **Busca** en la web: primero con `ddgs` (región `es-es`). Si salen menos de 10 resultados, completa leyendo directamente Bing y después Brave. Quita los repetidos (la misma página escrita de dos formas cuenta una vez) y los resultados que llegan pegados unos con otros.
2. **Mide el parecido** entre la búsqueda y cada resultado (título + extracto) con `paraphrase-multilingual-MiniLM-L12-v2`.
3. **Aplica la fórmula SSS** y ordena.
4. **Calcula el punto de sincronía** y marca con ◆ el resultado más sincronizado.
5. **Con Chrome y Gemini Nano**: Nano puntúa cada resultado de 0 a 10, el servidor fusiona esa nota con MiniLM, vuelve a aplicar SSS, reordena la página y Nano escribe una síntesis de 2 o 3 frases citando las fuentes como `[id]`.

## La matemática paso a paso

La fórmula está en [`motor_semantico_experimental.py`](motor_semantico_experimental.py). Cómo se aplica está en [`vaya_mono.py`](vaya_mono.py).

### 0. La entrada: similitud coseno

MiniLM convierte la búsqueda $q$ y cada resultado $d_i$ en vectores de 384 números. El parecido es el coseno del ángulo entre los dos vectores:

$$\alpha_i=\cos(\mathbf q,\mathbf d_i)=\frac{\mathbf q\cdot\mathbf d_i}{\|\mathbf q\|\,\|\mathbf d_i\|}\in[-1,1]$$

Con todos los resultados de una búsqueda se calculan dos parámetros:

$$\rho=10\cdot\frac{n}{20}\quad(n=\text{número de resultados, como máximo 20}),\qquad \sigma=\frac1n\sum_i\alpha_i$$

### 1. Fase S1: resonancia de Bessel

$$S_1(\alpha)=J_1(\alpha\rho)\cdot e^{-1{,}9041}$$

$J_1$ es la función de Bessel de primera especie y orden 1, y $e^{-1{,}9041}\approx 0{,}1490$. Con 20 resultados ($\rho=10$), $J_1(10\alpha)$ oscila mientras $\alpha$ va de 0 a 1 y pasa por cero en $\alpha\approx 0{,}383$ y $\alpha\approx 0{,}702$. Su tamaño está acotado: $|S_1|\le 0{,}582\cdot 0{,}149\approx 0{,}087$.

### 2. Fase S2: horizonte de Schwarzschild lógico

Tiene la forma del factor de Schwarzschild de la relatividad general, $1/\sqrt{1-r_s/r}$, con radio $r_s=2\alpha$ y distancia $r=1/\sigma$:

$$S_2(\alpha)=\begin{cases}\dfrac{1}{\sqrt{1-2\alpha\sigma}} & \text{si } 2\alpha\sigma<1\\[2mm] 100 & \text{si } 2\alpha\sigma\ge 1\ \text{(dentro del horizonte: atracción máxima)}\end{cases}$$

El horizonte está en $\alpha_h=1/(2\sigma)$. Cuanto más se acerca un resultado al horizonte, más crece $S_2$, sin límite. Al cruzarlo, $S_2$ se fija en 100.

### 3. Fase S3: aniquilación de fase

$$S_3(t)=\frac{k}{2}\big(J_0(kt)-J_2(kt)\big),\qquad k=1{,}832827,\quad t=1-\alpha$$

Por la identidad de Bessel $J_1'(x)=\tfrac12\big(J_0(x)-J_2(x)\big)$, esto es exactamente

$$S_3(t)=k\,J_1'(kt)=\frac{d}{dt}J_1(kt)$$

Es decir, S3 es la **derivada** de la misma función de Bessel de S1. Valores:

| $\alpha$ | 0 | 0,2 | 0,5 | 0,8 | 1 |
|---|---|---|---|---|---|
| $S_3(1-\alpha)$ | 0,0063 | 0,2812 | 0,6442 | 0,8707 | 0,9164 |

En $\alpha=0$ casi se anula porque $k=1{,}832827$ está muy cerca del primer cero de $J_1'$, que es $1{,}841184$ (un 0,45 % por encima). En $\alpha=1$ vale $k/2$.

### 4. La ecuación de unificación

$$\boxed{\ \text{SSS}(\alpha)=\max\Big(0,\ \alpha\cdot\big(S_1(\alpha)+S_2(\alpha)\big)\cdot\big|S_3(1-\alpha)\big|\Big)\ }$$

Como $S_2\ge 1$ y $|S_1|<0{,}09$, el paréntesis siempre es positivo. Los resultados se ordenan de mayor a menor SSS.

Valores con 20 resultados ($\rho=10$):

| $\alpha$ | 0,1 | 0,3 | 0,5 | 0,7 | 0,9 |
|---|---|---|---|---|---|
| SSS con $\sigma=0{,}2$ | 0,0157 | 0,1381 | 0,3444 | 0,6717 | 1,0478 |
| SSS con $\sigma=0{,}4$ | 0,0160 | 0,1482 | 0,4001 | 0,8593 | 1,5688 |
| SSS con $\sigma=0{,}6$ | 0,0164 | 0,1609 | 0,4936 | 1,4253 | 81,4704 |

Con $\sigma=0{,}6$, el resultado con $\alpha=0{,}9$ está más allá del horizonte ($\alpha_h=0{,}833$) y su valor se dispara.

### 5. El punto de sincronía $\alpha^*$

Es el valor en el que la fórmula SSS y MiniLM dan lo mismo, es decir, un **punto fijo**:

$$\text{SSS}(\alpha^*)=\alpha^*,\qquad \alpha^*\in(0,1]$$

Cómo se calcula (`punto_sincronia`): se evalúa $D(\alpha)=\text{SSS}(\alpha)-\alpha$ en 400 puntos entre $1/400$ y $1$. Se busca el primer cambio de signo y se afina con el **método de Brent** (`scipy.optimize.brentq`, tolerancia $10^{-12}$). Se deja fuera el punto trivial $\alpha=0$. Si no hay cruce, la página muestra «—».

| $\rho=10$ | $\sigma=0{,}2$ | $\sigma=0{,}4$ | $\sigma=0{,}6$ |
|---|---|---|---|
| $\alpha^*$ | 0,729227 | 0,602928 | 0,504248 |

El **resultado sincronizado ◆** es el que tiene el desfase relativo más pequeño:

$$\delta_i=\frac{|\text{SSS}(\alpha_i)-\alpha_i|}{\alpha_i}$$

Se mide en proporción para que los resultados irrelevantes, con valores casi nulos, no salgan siempre como "sincronizados". Si $\alpha_i\le 10^{-9}$, $\delta_i=10^9$.

### 6. Fusión con Gemini Nano

Nano da una nota $\nu_i\in[0,10]$. La entrada de SSS pasa a ser

$$\alpha_i^{\text{fusión}}=(1-w)\,\alpha_i+w\,\frac{\nu_i}{10},\qquad w=0{,}5$$

y se repiten los pasos 1 a 5 con $\sigma$ recalculada. Los resultados que Nano no puntúa conservan su $\alpha_i$.

### 7. Propiedad comprobada: SSS conserva el orden salvo en el horizonte

Se comprobó numéricamente con $\alpha\in[0,1]$ (20 001 puntos), $\rho\in\{0{,}5;\,2{,}5;\,5;\,7{,}5;\,10\}$ y $\sigma$ de 0,05 a 0,9. En todos los casos, SSS es **creciente** en $\alpha$ excepto justo en el horizonte $\alpha_h=1/(2\sigma)$, donde $S_2$ pasa de valores muy grandes a 100.

En consecuencia:

- Fuera del horizonte, **ordenar por SSS da el mismo orden que ordenar por la entrada** (MiniLM, o la fusión con Nano). La fórmula cambia la escala de las puntuaciones, separa mucho los resultados más cercanos al horizonte y define $\alpha^*$ y el resultado sincronizado.
- Un resultado justo por debajo del horizonte puede quedar por delante de otros que lo han cruzado.

## Arquitectura

```
 ventana Qt (navegador_pulsante.py) ──┐
                                      ├─► http://127.0.0.1:5002 ── servidor Flask (servidor_mono.py)
 Chrome --app (sss_chrome.py) ────────┘            │
        │                                          ├─ Buscador: ddgs → Bing → Brave
        │                                          ├─ MotorSemantico: MiniLM (CPU)
        │                                          └─ MotorPrincipal: SSS + punto de sincronía
        │
        └─ nano.js: Gemini Nano (Prompt API) ──► POST /api/fusion ──► nuevo orden + síntesis
```

- **Una búsqueda cada vez**, por orden de llegada (`TurnoBusqueda`). Ninguna se descarta.
- **Arranque bajo demanda**: con `sss-browser-2.socket` (systemd de usuario), systemd vigila el puerto 5002 y arranca el servidor con la primera búsqueda.
- **Apagado automático** tras 10 minutos sin peticiones. Las ventanas abiertas mandan un latido cada minuto para mantenerlo vivo.
- **Límites** del servicio: 3 GB de memoria y 3 núcleos.

### API del servidor

| Método y ruta | Qué devuelve |
|---|---|
| `GET /` | Portada |
| `GET /search?q=…` | Página de resultados |
| `GET /api/search?q=…` | JSON: `consulta`, `resultados` (con `alpha`, `alpha_base`, `desfase`, `desfase_rel`, `sincronizado`, `fuente`) y `sincronia` |
| `POST /api/fusion` | Recibe `{resultados: [{id, alpha_base}], nano: {id: 0..10}}` y devuelve el nuevo orden SSS |
| `GET /opensearch.xml` | Ficha OpenSearch para añadir SSS como buscador en Chrome o Firefox |
| `GET /api/estado` | `{"servicio": "sss-buscador"}`, para saber que quien contesta es SSS |
| `POST /api/latido` | Mantiene el servidor encendido |

## Instalación

Hace falta Python 3 con `venv` y conexión a Internet. El entorno ocupa varios GB, por PyTorch.

```bash
cd sss-browser
./instalar_entorno.sh "$PWD/venv"
```

El script instala PyTorch solo para procesador (unos 3,4 GB menos que la versión con CUDA) y el resto con las versiones fijadas en `requisitos.txt` y `restricciones.txt`. La primera vez se descarga el modelo MiniLM de Hugging Face.

Para Gemini Nano hace falta Google Chrome con la Prompt API. Si no aparece, actívala en `chrome://flags/#prompt-api-for-gemini-nano`.

## Uso

```bash
# Ventana propia (arranca el servidor si hace falta)
SSS_PUERTO=5002 venv/bin/python navegador_pulsante.py

# En Google Chrome, con Gemini Nano
SSS_PUERTO=5002 venv/bin/python sss_chrome.py

# Solo el servidor (apagado tras 600 s sin uso)
venv/bin/python servidor_mono.py 5002 --auto-apagado 600

# Desde la terminal
venv/bin/python vaya_mono.py "función zeta de Riemann"
```

En la barra de la ventana, una dirección (`es.wikipedia.org`) se abre como página web y cualquier otra cosa se busca con SSS. **PULSAR SSS** vuelve a la portada.

En la terminal, `vaya_mono.py` escribe primero el punto de sincronía α\*. Después, una línea por resultado con el valor SSS, el valor de MiniLM, el desfase relativo Δ, el título, la dirección y la marca ◆ en el resultado sincronizado.

## Paquete Debian

En `packaging/` están los lanzadores de `/usr/bin`, el servicio y el socket de systemd, los accesos directos y el icono del paquete `sss-browser-2_2.0.5-1_all.deb`. El paquete espera el entorno de Python en `/var/lib/sss-browser-2/venv`.

## Configuración

En `vaya_mono.py`, clase `Configuracion`:

| Parámetro | Valor | Significado |
|---|---|---|
| `MAX_RESULTADOS_WEB` | 20 | resultados por búsqueda |
| `MIN_RESULTADOS_WEB` | 10 | por debajo de esto se consulta Bing y Brave |
| `REGION` | `es-es` | región de ddgs |
| `MODELO_EMBEDDINGS` | `paraphrase-multilingual-MiniLM-L12-v2` | modelo de MiniLM |
| `PESO_NANO` | 0,5 | peso $w$ de Gemini Nano en la fusión |
| `REQUESTS_TIMEOUT` | 10 s | tiempo máximo por buscador |
