# backend/app.py

from flask import Flask
from backend.config import Config
from backend.models import db
from backend.routes import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
