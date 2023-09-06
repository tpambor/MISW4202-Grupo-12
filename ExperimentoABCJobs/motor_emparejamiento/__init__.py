from flask import Flask


# Fabrica de la app
def create_app(config_name):
    app = Flask(__name__)
    return app
