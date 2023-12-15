from flask import Flask
from app import handler

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to My Watchlist!"


@app.route("/model/<model>")
def query_model(model):
    return handler.query_model_and_chipsets(model)
