# Historial de cambios

## Radio Matemática

### 2.0.0-1

- Arreglos: base de datos y catálogo de canciones vuelven a guardarse
  (datos en ~/.local/share/radio-matematica-2 si la carpeta del programa
  no admite escritura); frecuencia dominante corregida (salía al doble);
  diario CSV en la carpeta de datos; errores avisados en vez de ocultos;
  registros pendientes guardados al cerrar.
- Ventana: indicadores con nombres reales; panel de los 20 modos en
  directo; botón MOTOR SÍ/NO para comparar con la emisora original;
  orbe circular; barra inferior visible en pantallas de 1080 píxeles.
- Sonido: modo más alto a 16 kHz (los 20 modos útiles con emisoras
  MP3); botón de pulso binaural real de 7,83 Hz (200 / 207,83 Hz,
  -30 dBFS), apagado al arrancar.
- Limpieza de código que no se ejecutaba.


_Wed, 28 Oct 2026 15:34:02 +0100_

## SSS Browser

### 2.0.5-1

- SSS como buscador de Chrome: las páginas publican una ficha OpenSearch
  (/opensearch.xml) para añadir SSS al buscador de la barra de Chrome.
- Servidor bajo demanda: sss-browser-2.socket (systemd de usuario) vigila
  el puerto 5002 y arranca SSS con la primera búsqueda; SSS se sigue
  apagando solo tras 10 min sin uso. Límite de 3 GB de memoria y 3 núcleos.
- La ventana y el lanzador de Chrome no arrancan un segundo servidor si
  systemd ya vigila el puerto.


_Thu, 29 Oct 2026 11:34:32 +0100_

### 2.0.4-1

- Versión visible: el número de versión sale en el nombre del menú, en
  una etiqueta del icono y en el título de la ventana.


_Thu, 29 Oct 2026 11:17:52 +0100_

### 2.0.3-1

- Interfaz: ventana oscura y moderna a juego con las páginas (botones
  redondeados, barra de dirección con borrado, línea de carga, sin
  fogonazo blanco); páginas con tarjetas, métricas en etiquetas y
  direcciones abreviadas (es.wikipedia.org › wiki › Mono). Mismas
  funciones y mismos botones.


_Thu, 29 Oct 2026 11:01:39 +0100_

### 2.0.2-1

- Servidor: las búsquedas se hacen de una en una, por orden de llegada;
  todas se hacen, ninguna se descarta (antes se hacían todas a la vez y
  una ráfaga de búsquedas saturaba el ordenador).
- Buscador: la misma página con la dirección escrita de dos formas
  (Natación / Nataci%C3%B3n) cuenta una sola vez.
- Buscador: dos copias iguales de un resultado ya no se eliminan entre
  sí al filtrar los resultados pegados.


_Thu, 29 Oct 2026 10:22:34 +0100_

### 2.0.1-1

- Buscador: se descartan los resultados que llegan pegados (título y
  texto de otro resultado dentro de uno).
- Página: extractos recortados a unas 320 letras; MiniLM y Nano siguen
  recibiendo el texto completo.


_Wed, 28 Oct 2026 20:38:34 +0100_

### 2.0.0-1

- Buscador: si ddgs trae menos de 10 resultados se completa leyendo
  Bing y Brave; sin repetidos; región España; la página dice de qué
  buscador viene cada resultado.
- Avisos: cuando el buscador falla la página lo dice, en vez de
  "Sin resultados"; la ventana avisa si el servidor no arranca.
- Ventana: sale al momento con "Cargando"; mantiene vivo el servidor
  y lo vuelve a arrancar si se apagó; la barra de arriba busca.
- Servidor: /api/estado para saber que quien contesta es SSS.
- Paquete: todos los archivos (plantillas, estáticos, sss_chrome.py);
  entorno propio con torch solo CPU y versiones fijas; puerto 5002;
  lanzador sin "fuser -k". La fórmula SSS no cambia.


_Wed, 28 Oct 2026 20:26:00 +0100_
