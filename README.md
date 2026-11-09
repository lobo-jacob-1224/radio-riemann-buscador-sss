# Radio de Riemann y buscador SSS

Dos programas de **Jacobo Cánovas García** que funcionan con la misma idea: **medir una señal real, pasar la medida por una fórmula matemática propia y usar el resultado para actuar sobre la señal**.

- **La radio** mide cuánta energía tiene la música en 20 bandas de frecuencia. Esas bandas están colocadas según los 20 primeros ceros de la función zeta de Riemann. Con esa medida, la radio realza las bandas donde suena la música y lo hace en directo, mientras la escuchas.
- **El buscador** mide con un modelo de lenguaje cuánto se parece cada resultado web a lo que has buscado. Esa medida pasa por la fórmula SSS (funciones de Bessel y un horizonte del tipo de Schwarzschild), que ordena los resultados y calcula un punto de equilibrio: el valor en el que la fórmula devuelve lo mismo que recibe.

| Proyecto | Qué es | Señal de entrada | Matemática central |
|---|---|---|---|
| [**Radio Matemática**](radio-matematica/) | Radio por Internet que procesa la emisora en tiempo real | Audio estéreo de 44,1 kHz | 20 ceros de la función zeta de Riemann colocados como filtros, con ganancias que siguen a la música |
| [**SSS Browser**](sss-browser/) | Buscador web con ventana propia | Resultados de búsqueda web | Similitud semántica (MiniLM) transformada por la fórmula SSS: Bessel, horizonte de Schwarzschild y derivada de Bessel |

Los dos están escritos en Python, funcionan en Linux y se han usado como paquetes Debian (`radio-matematica-2` 2.0.0 y `sss-browser-2` 2.0.5).

---

## La matemática en una página

### Radio Matemática: el filtro de los ceros de Riemann

Los ceros no triviales de la función zeta tienen la forma $\rho_n = \tfrac12 + i\gamma_n$. El motor toma los 20 primeros $\gamma_n$ (de 14,134725 a 77,144840) y los convierte en 20 frecuencias audibles con una escala logarítmica:

$$f_n = 50\,\text{Hz}\cdot\left(\frac{16000}{50}\right)^{\frac{\gamma_n-\gamma_1}{\gamma_{20}-\gamma_1}}$$

Cada $f_n$ es el centro de una campana de Gauss de 12 Hz de anchura. La ganancia $G_n(t)$ de cada campana sube cuando la música tiene energía en esa banda (en unos 0,9 s) y baja despacio cuando la pierde (en unos 23 s). El espectro de la emisora se multiplica por la máscara

$$M(f,t) = 0{,}6 + \sum_{n=1}^{20} G_n(t)\, e^{-\frac12\left(\frac{f-f_n}{12}\right)^2}$$

y se reconstruye con solapamiento y suma, más una saturación suave `tanh` con el volumen compensado. → [Explicación completa](radio-matematica/README.md#la-matemática-paso-a-paso)

### SSS Browser: la fórmula SSS

Para cada resultado, MiniLM da su parecido con la búsqueda, $\alpha\in[-1,1]$ (similitud coseno). La fórmula SSS lo transforma en tres fases:

$$\text{SSS}(\alpha)=\max\Big(0,\;\alpha\cdot\big[\underbrace{J_1(\alpha\rho)\,e^{-1{,}9041}}_{S_1}+\underbrace{\tfrac{1}{\sqrt{1-2\alpha\sigma}}}_{S_2}\big]\cdot\Big|\underbrace{\tfrac{k}{2}\big(J_0(k t)-J_2(k t)\big)}_{S_3}\Big|\Big),\qquad t=1-\alpha,\;k=1{,}832827$$

donde $\rho$ depende de cuántos resultados hay y $\sigma$ es la media de los $\alpha$. Cuando $2\alpha\sigma\ge 1$ (el horizonte), $S_2$ vale 100. El **punto de sincronía** $\alpha^*$ es el valor donde la fórmula devuelve lo mismo que recibe: $\text{SSS}(\alpha^*)=\alpha^*$. → [Explicación completa](sss-browser/README.md#la-matemática-paso-a-paso)

---

## Estructura del repositorio

```
radio-riemann-buscador-sss/
├── radio-matematica/          Radio Matemática 2.0.0
│   ├── engine.py              ventana, emisoras, audio, base de datos
│   ├── motor_convergencia_infinito.py   el motor matemático (filtro de Riemann)
│   ├── radio_cuantica.py      versión anterior, más simple (ver «Limitaciones»)
│   └── packaging/             lanzador, icono y acceso directo del paquete Debian
├── sss-browser/               SSS Browser 2.0.5
│   ├── motor_semantico_experimental.py  la fórmula SSS
│   ├── vaya_mono.py           búsqueda web, MiniLM, SSS y punto de sincronía
│   ├── servidor_mono.py       servidor web local (Flask)
│   ├── navegador_pulsante.py  ventana del navegador (Qt)
│   ├── sss_chrome.py          modo Google Chrome con Gemini Nano
│   ├── static/, templates/    páginas web
│   └── packaging/             lanzadores, servicio systemd, icono, accesos directos
├── CHANGELOG.md
└── LICENSE                    GNU GPL v3.0
```

## Inicio rápido

```bash
git clone https://github.com/lobo-jacob-1224/radio-riemann-buscador-sss.git
cd radio-riemann-buscador-sss
```

- Radio: [instalación y uso](radio-matematica/README.md#instalación)
- Buscador: [instalación y uso](sss-browser/README.md#instalación)

## Licencia

[GNU General Public License v3.0](LICENSE).

## Autor

**Jacobo Cánovas García**, España.
