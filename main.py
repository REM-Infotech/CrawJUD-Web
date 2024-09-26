import os
import json
import pathlib
from dotenv import dotenv_values

from app import create_app


if __name__ == "__main__":


    app = create_app()
    port = dotenv_values().get("PORT", 5000)
    app.run("0.0.0.0", port=int(port), debug=True)
