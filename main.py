from app import create_app


if __name__ == "__main__":

    app, port, debug = create_app()
    app.run("0.0.0.0", port=int(port), debug=debug)
