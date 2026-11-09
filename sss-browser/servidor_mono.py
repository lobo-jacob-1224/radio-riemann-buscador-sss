import argparse
import logging
import os
import signal
import threading
import time

from flask import Flask, abort, jsonify, render_template, request

from vaya_mono import Buscador, BusquedaFallida, Configuracion, MotorPrincipal, MotorSemantico

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("sss")

config = Configuracion()
motor_principal = MotorPrincipal(config, MotorSemantico(), Buscador(config))
app = Flask(__name__)

_ultima_actividad = time.monotonic()


class TurnoBusqueda:
    """One search at a time, in arrival order: each request takes a ticket and waits for its turn.
    Every search is still done in full (none is dropped); they just never run at the same time."""

    def __init__(self):
        self._cond = threading.Condition()
        self._siguiente = 0   # next ticket to hand out
        self._atendiendo = 0  # ticket whose turn it is now

    def __enter__(self):
        with self._cond:
            turno = self._siguiente
            self._siguiente += 1
            if turno != self._atendiendo:
                log.info("Búsqueda en cola: turno %d, %d por delante", turno, turno - self._atendiendo)
            while turno != self._atendiendo:
                self._cond.wait()
        return turno

    def __exit__(self, *exc):
        with self._cond:
            self._atendiendo += 1
            self._cond.notify_all()
        return False


turno_busqueda = TurnoBusqueda()


def buscar_en_turno(q):
    with turno_busqueda as turno:
        log.info("Buscando %r (turno %d)", q, turno)
        return motor_principal.ejecutar_ciclo(q)


@app.before_request
def _marcar_actividad():
    global _ultima_actividad
    _ultima_actividad = time.monotonic()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return render_template('home.html')
    try:
        resultados, sincronia = buscar_en_turno(q)
    except BusquedaFallida as e:
        return render_template('resultados.html', consulta=q, resultados=[], sincronia=None, error=str(e))
    return render_template('resultados.html', consulta=q, resultados=resultados, sincronia=sincronia)


@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if not q:
        abort(400, "Falta el parámetro q")
    try:
        resultados, sincronia = buscar_en_turno(q)
    except BusquedaFallida as e:
        return jsonify(consulta=q, error=str(e)), 502
    return jsonify(consulta=q, resultados=resultados, sincronia=sincronia)


@app.route('/opensearch.xml')
def opensearch():
    """Lets Chrome (or Firefox) add SSS as a search engine for its address bar."""
    base = request.host_url
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>Buscador SSS</ShortName>
  <Description>Buscador SSS: MiniLM y la fórmula SSS</Description>
  <InputEncoding>UTF-8</InputEncoding>
  <Url type="text/html" method="get" template="{base}search?q={{searchTerms}}"/>
</OpenSearchDescription>"""
    return app.response_class(xml, mimetype='application/opensearchdescription+xml')


@app.route('/api/estado')
def estado():
    """Identifies this server, so the window does not mistake another program on the port for SSS."""
    return jsonify(servicio='sss-buscador')


@app.route('/api/fusion', methods=['POST'])
def api_fusion():
    """Recibe los resultados de la página y las puntuaciones de Gemini Nano; devuelve el nuevo orden SSS."""
    datos = request.get_json(silent=True) or {}
    try:
        resultados = [{'id': int(r['id']), 'alpha_base': float(r['alpha_base'])} for r in datos['resultados']]
        puntuaciones = {int(k): float(v) for k, v in datos.get('nano', {}).items()}
    except (KeyError, TypeError, ValueError):
        abort(400, "Formato de fusión no válido")
    if not resultados or len(resultados) > config.MAX_RESULTADOS_WEB:
        abort(400, "Número de resultados no válido")
    fusion, sincronia = motor_principal.fusionar_nano(resultados, puntuaciones)
    campos = ('id', 'alpha', 'alpha_fusion', 'desfase', 'desfase_rel', 'sincronizado', 'nano')
    return jsonify(resultados=[{k: r[k] for k in campos if k in r} for r in fusion], sincronia=sincronia)


@app.route('/api/latido', methods=['POST'])
def latido():
    return ('', 204)


def _vigilar_inactividad(limite_s):
    while True:
        time.sleep(30)
        if time.monotonic() - _ultima_actividad > limite_s:
            log.info("Sin actividad durante %d s: apagando servidor SSS", limite_s)
            os.kill(os.getpid(), signal.SIGINT)  # apagado ordenado de Flask
            return


if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Servidor del buscador SSS")
    p.add_argument('puerto', nargs='?', type=int, default=5000)
    p.add_argument('--auto-apagado', type=int, default=0, metavar='SEG',
                   help="apagar tras SEG segundos sin peticiones (0 = nunca)")
    args = p.parse_args()
    if args.auto_apagado > 0:
        threading.Thread(target=_vigilar_inactividad, args=(args.auto_apagado,), daemon=True).start()
    try:
        if os.environ.get('LISTEN_FDS') == '1' and os.environ.get('LISTEN_PID') == str(os.getpid()):
            # Started by systemd socket activation (sss-browser-2.socket): the port is already
            # open as fd 3 and the first search is waiting on it.
            from werkzeug.serving import make_server
            log.info("Arrancado por systemd en el puerto %d", args.puerto)
            make_server('127.0.0.1', args.puerto, app, threaded=True, fd=3).serve_forever()
        else:
            app.run(host='127.0.0.1', port=args.puerto, threaded=True)
    except KeyboardInterrupt:
        pass
