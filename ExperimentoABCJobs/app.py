from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app_context = app.app_context()
app_context.push()


cors = CORS(app)
