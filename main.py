from clear import clear
from app import create_app
from eventlet import listen
from eventlet.wsgi import server
from dotenv import dotenv_values as values

if __name__ == "__main__":

    port = int(values().get("PORT", 5000))
    debug = values().get("DEBUG", "False").lower() in ("true", "1", "t", "y", "yes")
    app = create_app()
    if not debug:
        with open(".version", "w") as f:
            from app.misc.checkout import checkout_release_tag

            version = checkout_release_tag()
            f.write(version)

        clear()

        print("=======================================================\n")
        print("Executando servidor Flask")
        print(f" * Versão: {version}")
        print(" * Porta: 8000")
        print("\n=======================================================")

        server(listen(("localhost", port)), app, log=app.logger)

    elif debug:
        print("=======================================================\n")
        print("Executando servidor Flask")
        print(" * Porta: 8000")
        print("\n=======================================================")

        app.run(port=int(port), debug=debug)
