from app import create_app


if __name__ == "__main__":

    app, port, debug = create_app()
    app.run(port=int(port), debug=debug)
