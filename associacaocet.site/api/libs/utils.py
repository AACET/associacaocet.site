from flask import Flask
from os import listdir, path

def load_routes(app: Flask):
    for route in listdir("routes"):
        if route.endswith(".py") and path.isfile(path.join("routes", route)):
            route = route.removesuffix(".py")
            module = __import__(f"routes.{route}")
            module = eval(f"module.{route}")
            module.setup(app)