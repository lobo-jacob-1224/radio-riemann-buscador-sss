import html, os, sys, subprocess, time
from urllib.parse import quote_plus
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QColor
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton, QToolBar,
                               QProgressBar)
from PySide6.QtWebEngineWidgets import QWebEngineView

from sss_chrome import (ESPERA_MAX, LOG, PUERTO, URL, buscar_chrome, lanzar_servidor, servidor_activo,
                        servidor_gestionado)

LATIDO_MS = 60_000  # keeps the shared server alive while this window is open, whatever page it shows

PAGINA = """<!doctype html><html lang="es"><meta charset="utf-8"><title>{titulo}</title>
<body style="margin:0;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;
font-family:system-ui,sans-serif;background:#0b1120;color:#e2e8f0;text-align:center;padding:0 24px">
<h1 style="color:{color};font-size:2.4em">{titulo}</h1><p style="max-width:640px;line-height:1.6">{texto}</p>
</body></html>"""

# Same palette as static/sss.css, so the window and the pages look like one thing.
ESTILO = """
QMainWindow, QWidget#centro { background: #0b1120; }
QToolBar#barra { background: #111a2e; border: none; border-bottom: 1px solid #1f2a44; padding: 8px 12px; spacing: 6px; }
QPushButton { color: #e2e8f0; background: transparent; border: none; border-radius: 17px;
              min-height: 34px; padding: 0 14px; font-size: 14px; }
QPushButton:hover { background: #1f2a44; }
QPushButton:pressed { background: #2a3858; }
QPushButton#nav { min-width: 34px; max-width: 34px; padding: 0; font-size: 18px; color: #94a3b8; }
QPushButton#nav:hover { color: #e2e8f0; }
QPushButton#pulsar { background: #38bdf8; color: #0b1120; font-weight: bold; }
QPushButton#pulsar:hover { background: #7dd3fc; }
QPushButton#chrome { border: 1px solid #2a3858; color: #cbd5e1; }
QLineEdit#direccion { background: #0b1120; color: #e2e8f0; border: 1px solid #2a3858; border-radius: 17px;
                      min-height: 34px; padding: 0 16px; font-size: 14px; selection-background-color: #38bdf8; }
QLineEdit#direccion:focus { border: 1px solid #38bdf8; }
QProgressBar#carga { background: transparent; border: none; max-height: 2px; }
QProgressBar#carga::chunk { background: #38bdf8; }
QToolTip { background: #111a2e; color: #e2e8f0; border: 1px solid #2a3858; padding: 4px 8px; }
"""

class Nav(QMainWindow):
    def __init__(self):
        super().__init__()
        version = os.environ.get("SSS_VERSION")  # set by the /usr/bin/sss-browser-2 launcher
        self.setWindowTitle("SSS v3.1 - Volátil" + (f" · versión {version}" if version else ""))
        self.resize(1100, 750)
        self.setStyleSheet(ESTILO)
        cw = QWidget()
        cw.setObjectName("centro")
        self.setCentralWidget(cw)
        lay = QVBoxLayout(cw)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        tb = QToolBar()
        tb.setObjectName("barra")
        tb.setMovable(False)
        tb.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.addToolBar(tb)

        # Botones de navegación
        btn_back = QPushButton("‹")
        btn_back.setObjectName("nav")
        btn_back.setToolTip("Atrás")
        btn_back.clicked.connect(lambda: self.vw.back())
        tb.addWidget(btn_back)

        btn_fwd = QPushButton("›")
        btn_fwd.setObjectName("nav")
        btn_fwd.setToolTip("Adelante")
        btn_fwd.clicked.connect(lambda: self.vw.forward())
        tb.addWidget(btn_fwd)

        btn_reload = QPushButton("↻")
        btn_reload.setObjectName("nav")
        btn_reload.setToolTip("Recargar")
        btn_reload.clicked.connect(lambda: self.vw.reload())
        tb.addWidget(btn_reload)

        self.ub = QLineEdit()
        self.ub.setObjectName("direccion")
        self.ub.setPlaceholderText("Dirección o búsqueda SSS")
        self.ub.setClearButtonEnabled(True)
        self.ub.returnPressed.connect(self.go)
        tb.addWidget(self.ub)

        b = QPushButton("PULSAR SSS")
        b.setObjectName("pulsar")
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(self.home)
        tb.addWidget(b)

        bn = QPushButton("Abrir en Chrome (Nano)")
        bn.setObjectName("chrome")
        bn.setToolTip("Gemini Nano solo está disponible dentro de Google Chrome")
        bn.setCursor(Qt.CursorShape.PointingHandCursor)
        bn.clicked.connect(self.abrir_chrome)
        tb.addWidget(bn)

        # Thin loading line under the bar: shows that a search is running
        self.carga = QProgressBar()
        self.carga.setObjectName("carga")
        self.carga.setTextVisible(False)
        self.carga.setFixedHeight(2)
        self.carga.hide()
        lay.addWidget(self.carga)

        self.vw = QWebEngineView()
        self.vw.page().setBackgroundColor(QColor("#0b1120"))  # no white flash while a page loads
        self.vw.urlChanged.connect(lambda q: self.ub.setText("" if q.scheme() in ("data", "about") else q.toString()))
        self.vw.loadStarted.connect(lambda: (self.carga.setValue(5), self.carga.show()))
        self.vw.loadProgress.connect(lambda p: self.carga.setValue(max(p, 5)))
        self.vw.loadFinished.connect(lambda _ok: self.carga.hide())
        lay.addWidget(self.vw)

        # Server start without freezing the window: launch, then poll every 0.5 s.
        self.proc = None
        self.destino = URL
        self.fin_espera = 0.0
        self.espera = QTimer(self)
        self.espera.timeout.connect(self._comprobar_servidor)

        self.red = QNetworkAccessManager(self)
        self.latido = QTimer(self)
        self.latido.timeout.connect(self._latido)
        self.latido.start(LATIDO_MS)

        self.home()

    def home(self): self.abrir(URL)
    def abrir_chrome(self):
        url = self.vw.url().toString() or URL
        subprocess.Popen([buscar_chrome(), f"--app={url}", "--class=sss-browser"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    def go(self):
        u = self.ub.text().strip()
        if not u:
            return
        if u.startswith(URL):
            self.abrir(u)
        elif u.startswith(("http://", "https://")):
            self.vw.setUrl(QUrl(u))
        elif " " not in u and "." in u:
            self.vw.setUrl(QUrl("http://" + u))
        else:
            # Not an address: search it with SSS
            self.abrir(f"{URL}search?q={quote_plus(u)}")

    def abrir(self, url):
        """Open an SSS page, starting the server first if it is not running (first start or auto-shutdown)."""
        if servidor_activo():
            self.vw.setUrl(QUrl(url))
            return
        self.destino = url
        if self.espera.isActive():
            return
        self._pagina("#38bdf8", "Cargando SSS…",
                     "Arrancando el servidor y el modelo MiniLM. La primera vez puede tardar hasta un minuto y medio.")
        if servidor_gestionado():
            self.proc = None  # systemd starts the server itself on the first connection
        elif self.proc is None or self.proc.poll() is not None:
            self.proc = lanzar_servidor()
        self.fin_espera = time.monotonic() + ESPERA_MAX
        self.espera.start(500)

    def _comprobar_servidor(self):
        if servidor_activo():
            self.espera.stop()
            self.vw.setUrl(QUrl(self.destino))
        elif self.proc is not None and self.proc.poll() is not None:
            self.espera.stop()
            self._pagina("#f87171", "El servidor SSS no ha arrancado",
                         f"Terminó con código {self.proc.returncode}. Puede que otro programa esté usando "
                         f"el puerto {PUERTO}. El detalle está en {LOG}. Pulsa PULSAR SSS para reintentar.")
        elif time.monotonic() > self.fin_espera:
            self.espera.stop()
            self._pagina("#f87171", "El servidor SSS no responde",
                         f"No contestó en {ESPERA_MAX} s. El detalle está en {LOG}. Pulsa PULSAR SSS para reintentar.")

    def _pagina(self, color, titulo, texto):
        self.vw.setHtml(PAGINA.format(color=color, titulo=html.escape(titulo), texto=html.escape(texto)))

    def _latido(self):
        req = QNetworkRequest(QUrl(URL + "api/latido"))
        req.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "text/plain")
        reply = self.red.post(req, b"")
        reply.finished.connect(reply.deleteLater)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Nav()
    w.show()
    sys.exit(app.exec())
