from flask import Flask

app = Flask(__name__)


@app.route('/')
def Autorizador():
    return 'Autorizador!'