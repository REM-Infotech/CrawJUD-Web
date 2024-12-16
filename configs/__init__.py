import os
import shutil
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

from dotenv import dotenv_values


class Configurator:

    env_file = ".env"

    def __init__(self):

        debug_flag = Path(".debug").exists()
        if debug_flag:
            self.env_file = ".testing"

    def get_configurator(self):  # pragma: no cover

        class ConfigObject:

            values = dotenv_values(self.env_file)

            login_db = values.get("login")
            passwd_db = values.get("password")
            host_db = values.get("host")
            database_name = values.get("database")

            # FLASK-MAIL CONFIG
            MAIL_SERVER = values["MAIL_SERVER"]
            MAIL_PORT = int(values["MAIL_PORT"])
            MAIL_USE_TLS = False
            MAIL_USE_SSL = False
            MAIL_USERNAME = values["MAIL_USERNAME"]
            MAIL_PASSWORD = values["MAIL_PASSWORD"]
            MAIL_DEFAULT_SENDER = values["MAIL_DEFAULT_SENDER"]

            # SQLALCHEMY CONFIG
            DEBUG = values.get("DEBUG", "False").lower() in (
                "true",
                "1",
                "t",
                "y",
                "yes",
            )

            # SqlAlchemy config

            SQLALCHEMY_POOL_SIZE = 30  # Número de conexões na pool
            SQLALCHEMY_MAX_OVERFLOW = 10  # Número de conexões extras além da pool_size
            SQLALCHEMY_POOL_TIMEOUT = 30  # Tempo de espera para obter uma conexão
            SQLALCHEMY_POOL_RECYCLE = (
                1800  # Tempo (em segundos) para reciclar as conexões ociosas
            )
            SQLALCHEMY_POOL_PRE_PING = (
                True  # Verificar a saúde da conexão antes de usá-la
            )

            SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{login_db}:{passwd_db}@{host_db}/{database_name}"
            SQLALCHEMY_BINDS = {"cachelogs": "sqlite:///cachelogs.db"}
            SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
            SQLALCHEMY_TRACK_MODIFICATIONS = False

            # FLASK CONFIG
            PREFERRED_URL_SCHEME = "https"
            SESSION_COOKIE_HTTPONLY = False
            SESSION_COOKIE_SECURE = True
            PERMANENT_SESSION_LIFETIME = timedelta(days=31).max.seconds
            SECRET_KEY = str(uuid4())

            # File paths config
            PDF_PATH = os.path.join(os.getcwd(), "PDF")
            DOCS_PATH = os.path.join(os.getcwd(), "Docs")
            TEMP_PATH = os.path.join(os.getcwd(), "Temp")
            IMAGE_TEMP_PATH = os.path.join(TEMP_PATH, "IMG")
            CSV_TEMP_PATH = os.path.join(TEMP_PATH, "csv")
            PDF_TEMP_PATH = os.path.join(TEMP_PATH, "pdf")
            SRC_IMG_PATH = os.path.join(os.getcwd(), "app", "src", "assets", "img")

            for paths in [
                DOCS_PATH,
                TEMP_PATH,
                IMAGE_TEMP_PATH,
                CSV_TEMP_PATH,
                PDF_TEMP_PATH,
            ]:
                if Path(paths).exists():
                    shutil.rmtree(paths)

                Path(paths).mkdir(exist_ok=True)

        return ConfigObject


def csp() -> dict[str]:

    from app.models import Servers

    srvs = Servers.query.all()
    csp_vars = {
        "default-src": ["'self'"],
        "script-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://code.jquery.com",
            "https://use.fontawesome.com",
            "",
            "'unsafe-inline'",
        ],
        "style-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://github.com",
            "https://avatars.githubusercontent.com",
            "'unsafe-inline'",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://cdn-icons-png.flaticon.com",
            "https://github.com",
            "https://domain.cliente.com",
            "https://avatars.githubusercontent.com",
            "https://cdn-icons-png.freepik.com",
        ],
        "connect-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://github.com",
            "https://unpkg.com",
            "https://avatars.githubusercontent.com",
        ],
        "frame-src": [
            "'self'",
            "https://domain.cliente.com",
            "https://github.com",
            "https://avatars.githubusercontent.com",
        ],
    }
    if srvs:
        for srv in srvs:
            csp_vars.get("connect-src").append(f"https://{srv.address}")
            csp_vars.get("connect-src").append(f"wss://{srv.address}")

    return csp_vars
