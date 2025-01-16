from os import getcwd, path
from pathlib import Path

from clear import clear
from dotenv import dotenv_values as values
from eventlet import listen
from eventlet.wsgi import server

from app import create_app

app = create_app()

if __name__ == "__main__":

    clear()

    port = int(values().get("PORT", 5000))
    version_Path = Path(path.join(getcwd(), ".version"))

    if version_Path.exists() is False:
        from app.misc.checkout import checkout_release_tag

        with open(".version", "w") as f:
            f.write(checkout_release_tag())

    server(listen(("localhost", port)), app, log=app.logger)
