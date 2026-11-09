// Acoplamiento SSS <-> Gemini Nano (Prompt API integrada en Chrome).
// El modelo se ejecuta dentro de Chrome; aquí solo se le hacen consultas y
// sus puntuaciones se fusionan en Python con MiniLM y la fórmula SSS.
(() => {
  'use strict';

  const estado = document.getElementById('estado-nano');
  const botonActivar = document.getElementById('activar-nano');
  const datosEl = document.getElementById('datos-sss');
  const datos = datosEl ? JSON.parse(datosEl.textContent) : null;
  const cancelar = new AbortController();

  const OPCIONES = {
    expectedInputs: [{ type: 'text', languages: ['es', 'en'] }],
    expectedOutputs: [{ type: 'text', languages: ['es'] }],
  };
  const SISTEMA = 'Eres el motor de relevancia del buscador SSS. ' +
    'Respondes siempre en español, con precisión y brevedad, sin inventar datos que no estén en los resultados.';
  const ESQUEMA_PUNTUACIONES = {
    type: 'object',
    properties: {
      puntuaciones: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            id: { type: 'integer' },
            relevancia: { type: 'integer', minimum: 0, maximum: 10 },
          },
          required: ['id', 'relevancia'],
        },
      },
    },
    required: ['puntuaciones'],
  };
  const LARGO_EXTRACTO = 200;
  const RESULTADOS_SINTESIS = 5;

  function ponerEstado(clase, texto, ayuda = '') {
    estado.className = `nano nano-${clase}`;
    estado.textContent = texto;
    estado.title = ayuda || 'Estado de Gemini Nano';
  }

  const recortar = (s, n) => (s.length > n ? s.slice(0, n) + '…' : s);

  // Mantiene vivo el servidor mientras la ventana esté abierta (ver --auto-apagado).
  setInterval(() => fetch('/api/latido', { method: 'POST' }).catch(() => {}), 60_000);
  addEventListener('pagehide', () => cancelar.abort());

  async function disponibilidad() {
    if (!('LanguageModel' in self)) return 'sin-api';
    try {
      return await LanguageModel.availability(OPCIONES);
    } catch (e) {
      console.warn('SSS/Nano availability:', e);
      return 'unavailable';
    }
  }

  function crearSesion() {
    return LanguageModel.create({
      ...OPCIONES,
      initialPrompts: [{ role: 'system', content: SISTEMA }],
      signal: cancelar.signal,
      monitor(m) {
        m.addEventListener('downloadprogress', (e) =>
          ponerEstado('descargando', `Nano: descargando ${Math.round(e.loaded * 100)} %`));
      },
    });
  }

  function construirPrompt(conExtractos) {
    const lista = datos.resultados.map((r) => {
      const extracto = conExtractos && r.body ? `\n${recortar(r.body, LARGO_EXTRACTO)}` : '';
      return `[${r.id}] ${r.title}${extracto}`;
    }).join('\n\n');
    return `Consulta: "${datos.consulta}"\n\n` +
      'Puntúa de 0 a 10 la relevancia de cada resultado para la consulta ' +
      '(10 = responde exactamente a lo buscado, 0 = no tiene relación). Incluye todos los ids.\n\n' + lista;
  }

  async function puntuar(base) {
    const sesion = await base.clone({ signal: cancelar.signal });
    try {
      let prompt = construirPrompt(true);
      // Si los extractos no caben en el contexto de Nano, se puntúa solo con los títulos.
      if (sesion.measureInputUsage &&
          await sesion.measureInputUsage(prompt) > sesion.inputQuota - sesion.inputUsage - 512) {
        prompt = construirPrompt(false);
      }
      const texto = await sesion.prompt(prompt, {
        responseConstraint: ESQUEMA_PUNTUACIONES,
        signal: cancelar.signal,
      });
      const puntuaciones = {};
      for (const p of JSON.parse(texto).puntuaciones) {
        if (Number.isInteger(p.id) && Number.isFinite(p.relevancia)) puntuaciones[p.id] = p.relevancia;
      }
      return puntuaciones;
    } finally {
      sesion.destroy();
    }
  }

  async function fusionar(puntuaciones) {
    const resp = await fetch('/api/fusion', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resultados: datos.resultados.map((r) => ({ id: r.id, alpha_base: r.alpha_base })),
        nano: puntuaciones,
      }),
      signal: cancelar.signal,
    });
    if (!resp.ok) throw new Error(`Fusión SSS: HTTP ${resp.status}`);
    return resp.json();
  }

  function reordenar({ resultados: fusion, sincronia }) {
    const lista = document.getElementById('lista');
    const alphaSinc = document.getElementById('alpha-sincronia');
    if (alphaSinc) alphaSinc.textContent = sincronia == null ? '—' : sincronia.toFixed(6);
    fusion.forEach((r) => {
      const art = lista.querySelector(`.resultado[data-id="${r.id}"]`);
      if (!art) return;
      art.querySelector('.alpha').textContent = r.alpha.toFixed(6);
      art.querySelector('.desfase b').textContent = r.desfase.toFixed(6);
      art.querySelector('.desfase i').textContent = `${(r.desfase_rel * 100).toFixed(1)} %`;
      art.classList.toggle('sincronizado', r.sincronizado);
      if (r.nano !== undefined) {
        const n = art.querySelector('.nano-punt');
        n.querySelector('b').textContent = r.nano;
        n.hidden = false;
      }
      art.classList.add('fusionado');
      lista.appendChild(art);
    });
  }

  async function sintetizar(base, fusion) {
    const porId = new Map(datos.resultados.map((r) => [r.id, r]));
    const mejores = fusion.slice(0, RESULTADOS_SINTESIS).map((f) => porId.get(f.id)).filter(Boolean);
    if (!mejores.length) return;

    const contexto = mejores.map((r) => `[${r.id}] ${r.title}: ${recortar(r.body || '', 300)}`).join('\n');
    const prompt = `Consulta: "${datos.consulta}"\n\nResultados más resonantes:\n${contexto}\n\n` +
      'Escribe una síntesis de 2 o 3 frases que responda a la consulta usando solo esta información. ' +
      'Cita las fuentes como [id].';

    const seccion = document.getElementById('sintesis');
    const salida = document.getElementById('sintesis-texto');
    const sesion = await base.clone({ signal: cancelar.signal });
    try {
      seccion.hidden = false;
      salida.textContent = '';
      for await (const trozo of sesion.promptStreaming(prompt, { signal: cancelar.signal })) {
        salida.textContent += trozo;
      }
    } finally {
      sesion.destroy();
    }
  }

  async function acoplar(base) {
    if (!datos || !datos.resultados.length) {
      ponerEstado('activo', 'Nano: activo');
      return;
    }
    ponerEstado('trabajando', 'Nano: evaluando resonancia…');
    const fusion = await fusionar(await puntuar(base));
    reordenar(fusion);
    ponerEstado('trabajando', 'Nano: sintetizando…');
    await sintetizar(base, fusion.resultados);
    ponerEstado('activo', 'Nano: activo · SSS fusionado');
  }

  async function iniciar() {
    let base;
    try {
      base = await crearSesion();
      await acoplar(base);
    } catch (e) {
      if (e.name === 'AbortError') return;
      console.error('SSS/Nano:', e);
      // El orden SSS de MiniLM ya está en la página: solo se informa del fallo.
      ponerEstado('error', 'Nano: error · orden SSS básico',
        `${e.name}: ${e.message}. Revisa chrome://on-device-internals`);
    } finally {
      base?.destroy();
    }
  }

  async function main() {
    const disp = await disponibilidad();
    switch (disp) {
      case 'available':
        iniciar();
        break;
      case 'downloadable':
      case 'downloading':
        // Chrome exige un gesto del usuario para iniciar/continuar la descarga del modelo.
        ponerEstado('descargando', 'Nano: pendiente de activar');
        botonActivar.hidden = false;
        botonActivar.addEventListener('click', () => {
          botonActivar.hidden = true;
          iniciar();
        }, { once: true });
        break;
      case 'sin-api':
        ponerEstado('inactivo', 'Nano: no disponible',
          'Este navegador no expone la Prompt API. Abre SSS con Google Chrome (orden sss-browser-2-chrome o botón «Abrir en Chrome») ' +
          'y activa chrome://flags/#prompt-api-for-gemini-nano si hiciera falta.');
        break;
      default:
        ponerEstado('inactivo', 'Nano: no compatible',
          'Chrome indica que Gemini Nano no está disponible en este equipo o idioma.');
    }
  }

  main();
})();
