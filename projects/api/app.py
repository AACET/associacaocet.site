from flask import Flask
from libs import utils


app = Flask(__name__)

if __name__ == "app":
    utils.load_routes(app)