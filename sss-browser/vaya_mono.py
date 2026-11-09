#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys

import numpy as np
from scipy.optimize import brentq

from motor_semantico_experimental import transformar_alpha_experimental

log = logging.getLogger("sss")


class Configuracion:
    REQUESTS_TIMEOUT = 10
    UMBRAL_RELEVANCIA = 0.3
    MAX_RESULTADOS_WEB = 20
    # Below this many results from ddgs, Bing and then Brave are asked as well
    MIN_RESULTADOS_WEB = 10
    # Search region for ddgs (its default is the United States, in English)
    REGION = 'es-es'
    MODELO_EMBEDDINGS = 'paraphrase-multilingual-MiniLM-L12-v2'
    # Peso de Gemini Nano en la fusión (0 = solo MiniLM, 1 = solo Nano)
    PESO_NANO = 0.5


class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def punto_sincronia(rho, sigma, pasos=400):
    """Sincronizador SSS: alpha* en [0, 1] donde SSS(alpha*) == alpha* (los dos motores coinciden).

    Busca el primer cambio de signo de SSS(a) - a y lo refina con Brent. Se excluye el
    punto trivial a = 0 (ahí ambos motores valen 0). None si no hay cruce.
    """
    def desfase(a):
        return transformar_alpha_experimental(a, rho, sigma) - a

    malla = np.linspace(1.0 / pasos, 1.0, pasos)
    valores = [desfase(a) for a in malla]
    for a, b, fa, fb in zip(malla, malla[1:], valores, valores[1:]):
        if fa == 0.0:
            return float(a)
        if fa * fb < 0:
            return float(brentq(desfase, a, b, xtol=1e-12))
    return None


class MotorSemantico:
    def __init__(self, nombre_modelo=Configuracion.MODELO_EMBEDDINGS):
        from sentence_transformers import SentenceTransformer, util
        self.util = util
        self.modelo = SentenceTransformer(nombre_modelo, device='cpu')

    def calcular_alphas(self, textos, origen):
        """Similitud coseno de cada texto con el origen, en un único lote."""
        if not textos or not origen:
            return [0.0] * len(textos)
        emb_o = self.modelo.encode(origen, convert_to_tensor=True, show_progress_bar=False)
        emb_t = self.modelo.encode(textos, convert_to_tensor=True, batch_size=32, show_progress_bar=False)
        return self.util.cos_sim(emb_t, emb_o).squeeze(1).tolist()

    def calcular_alpha(self, texto, origen):
        return self.calcular_alphas([texto], origen)[0]


class BusquedaFallida(Exception):
    """The web search itself failed (blocked, timeout, network), as opposed to finding nothing."""


class Buscador:
    """Web search with fallbacks: ddgs first; if it brings fewer than MIN_RESULTADOS_WEB,
    Bing and Brave are read directly (their pages still answer when ddgs is blocked).
    Each result carries 'fuente' with the engine it came from; duplicates are dropped."""

    UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Chrome/151.0.0.0 Safari/537.36')

    def __init__(self, config):
        from ddgs import DDGS
        self.config = config
        self.DDGS = DDGS

    def buscar(self, consulta, max_resultados=20):
        resultados, errores, vistos = [], [], set()
        for nombre, motor in (('ddgs', self._ddgs), ('Bing', self._bing), ('Brave', self._brave)):
            if len(resultados) >= min(self.config.MIN_RESULTADOS_WEB, max_resultados):
                break
            try:
                nuevos = motor(consulta, max_resultados)
            except Exception as e:
                log.warning("Fallo en %s para %r: %s: %s", nombre, consulta, type(e).__name__, e)
                errores.append(f"{nombre}: {type(e).__name__}: {e}")
                continue
            log.info("%s: %d resultados para %r", nombre, len(nuevos), consulta)
            for r in nuevos:
                clave = self._clave(r['href'])
                if (clave in vistos or not r.get('title')
                        or not r['href'].startswith(('http://', 'https://'))):
                    continue
                vistos.add(clave)
                r['fuente'] = nombre
                resultados.append(r)
                if len(resultados) >= max_resultados:
                    break
        if not resultados and errores:
            raise BusquedaFallida(" · ".join(errores))
        return self._sin_pegotes(resultados)

    @staticmethod
    def _sin_pegotes(resultados):
        """Drop results glued together by an engine parser: a result whose title contains the
        title of another result AND whose text contains that other result's text (seen with
        ddgs on 28-10-2026: three titles and three snippets joined in one entry)."""
        limpios = []
        for r in resultados:
            otros = [o for o in resultados if o is not r]
            # A glued entry is always longer than the one it contains; equal titles are two copies
            # of the same page, not a glue, and must not knock each other out.
            pegote = any(len(o['title']) >= 8 and len(r['title']) > len(o['title']) and o['title'] in r['title']
                         and len(o['body']) >= 40 and o['body'][:80] in r['body'] for o in otros)
            if pegote:
                log.info("Descartado resultado pegado: %r", r['title'][:80])
            else:
                limpios.append(r)
        return limpios

    def _ddgs(self, consulta, max_resultados):
        with self.DDGS(timeout=self.config.REQUESTS_TIMEOUT) as ddgs:
            return [{'title': r.get('title', ''), 'href': r.get('href', ''), 'body': r.get('body', '')}
                    for r in ddgs.text(consulta, region=self.config.REGION, max_results=max_resultados)]

    def _pagina(self, url, params):
        import urllib.parse
        import urllib.request
        from lxml import html
        req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}", headers={
            'User-Agent': self.UA, 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.6'})
        with urllib.request.urlopen(req, timeout=self.config.REQUESTS_TIMEOUT) as resp:
            return html.fromstring(resp.read())

    @staticmethod
    def _texto(nodos):
        return " ".join(nodos[0].text_content().split()) if nodos else ''

    def _bing(self, consulta, max_resultados):
        doc = self._pagina('https://www.bing.com/search', {'q': consulta, 'setlang': 'es'})
        salida = []
        for li in doc.xpath('//li[contains(@class, "b_algo")]'):
            a = li.xpath('.//h2/a[@href]')
            if a:
                salida.append({'title': self._texto(a), 'href': self._bing_destino(a[0].get('href')),
                               'body': self._texto(li.xpath('.//p'))})
        return salida[:max_resultados]

    @staticmethod
    def _bing_destino(href):
        """Bing wraps links as bing.com/ck/a?...&u=a1<base64url of the real URL>."""
        import base64
        import urllib.parse
        if '/ck/a' not in href:
            return href
        u = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('u', [''])[0]
        if u.startswith('a1'):
            try:
                return base64.urlsafe_b64decode(u[2:] + '=' * (-len(u[2:]) % 4)).decode()
            except ValueError:
                pass
        return href

    def _brave(self, consulta, max_resultados):
        doc = self._pagina('https://search.brave.com/search', {'q': consulta, 'source': 'web'})
        salida = []
        for sn in doc.xpath('//div[contains(@class, "snippet") and @data-type="web"]'):
            a = sn.xpath('.//a[@href]')
            if a:
                salida.append({
                    'title': self._texto(sn.xpath('.//*[contains(@class, "search-snippet-title")]')),
                    'href': a[0].get('href'),
                    'body': self._texto(sn.xpath('.//div[contains(concat(" ", @class, " "), " content ")]'))})
        return salida[:max_resultados]

    @staticmethod
    def _clave(href):
        """Same page reached through http/https, www, a trailing slash or percent-encoding
        (Natación / Nataci%C3%B3n) counts once."""
        import urllib.parse
        p = urllib.parse.urlparse(href)
        host = p.netloc.lower().removeprefix('www.')
        return f"{host}{urllib.parse.unquote(p.path).rstrip('/')}?{urllib.parse.unquote(p.query)}"


class MotorPrincipal:
    def __init__(self, config, motor_semantico, buscador):
        self.config = config
        self.motor_semantico = motor_semantico
        self.buscador = buscador

    def ejecutar_ciclo(self, consulta):
        resultados = self.buscador.buscar(consulta, max_resultados=self.config.MAX_RESULTADOS_WEB)
        if not resultados:
            return [], None

        textos = [f"{r['title']}. {r['body']}" if r['body'] else r['title'] for r in resultados]
        for i, (r, a) in enumerate(zip(resultados, self.motor_semantico.calcular_alphas(textos, consulta))):
            r['id'] = i
            r['alpha_base'] = a
        return self.aplicar_sss(resultados, 'alpha_base')

    def fusionar_nano(self, resultados, puntuaciones_nano):
        """Combina alpha_base (MiniLM) con la relevancia 0-10 de Gemini Nano y reaplica SSS.

        resultados: lista con 'id' y 'alpha_base'. puntuaciones_nano: {id: 0..10}.
        Los resultados sin puntuación de Nano conservan solo su alpha_base.
        """
        w = self.config.PESO_NANO
        for r in resultados:
            nano = puntuaciones_nano.get(r['id'])
            if nano is None:
                r['alpha_fusion'] = r['alpha_base']
            else:
                r['nano'] = nano
                r['alpha_fusion'] = (1 - w) * r['alpha_base'] + w * (min(max(nano, 0.0), 10.0) / 10.0)
        return self.aplicar_sss(resultados, 'alpha_fusion')

    def aplicar_sss(self, resultados, campo):
        """Aplica SSS y ordena por relevancia SSS. La sincronía es informativa: se marca el
        resultado donde SSS y su entrada (MiniLM, o la fusión MiniLM+Nano) están más cerca
        de ser iguales.

        La igualdad se mide en proporción (|SSS - entrada| / entrada): es 0 en alpha* y no
        premia a los resultados irrelevantes, cuyos valores casi nulos siempre están cerca.
        Devuelve (resultados_ordenados, alpha_sincronia).
        """
        rho = len(resultados) / self.config.MAX_RESULTADOS_WEB * 10.0
        sigma = float(np.mean([r[campo] for r in resultados]))
        for r in resultados:
            r['alpha'] = transformar_alpha_experimental(r[campo], rho, sigma)
            r['desfase'] = abs(r['alpha'] - r[campo])
            # Entrada nula o negativa: sin sincronía posible, al final (valor finito, válido en JSON).
            r['desfase_rel'] = r['desfase'] / r[campo] if r[campo] > 1e-9 else 1e9
            r['sincronizado'] = False
        min(resultados, key=lambda x: x['desfase_rel'])['sincronizado'] = True
        orden = sorted(resultados, key=lambda x: x['alpha'], reverse=True)
        return orden, punto_sincronia(rho, sigma)


if __name__ == "__main__":
    conf = Configuracion()
    m_principal = MotorPrincipal(conf, MotorSemantico(), Buscador(conf))

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "función zeta de Riemann"
    try:
        resultados, sincronia = m_principal.ejecutar_ciclo(query)
    except BusquedaFallida as e:
        sys.exit(f"{C.RED}El buscador ha fallado: {e}{C.END}")
    if sincronia is not None:
        print(f"{C.CYAN}Punto de sincronía α* = {sincronia:.6f}{C.END}")
    for r in resultados:
        marca = f" {C.YELLOW}◆ sincronizado{C.END}" if r['sincronizado'] else ""
        print(f"{C.GREEN}SSS {r['alpha']:.6f}{C.END} | MiniLM {r['alpha_base']:.6f} | Δ {r['desfase_rel']:.1%}"
              f" | {r['title']} | {r['href']}{marca}")
