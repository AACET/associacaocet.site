from flask import Blueprint, Flask

route = Blueprint("members", __name__, url_prefix='/members')

@route.route("/status")
def status():
    return {'status': 200}


def setup(app: Flask):
    app.register_blueprint(route)
