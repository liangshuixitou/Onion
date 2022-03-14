from flask import Flask


def create_app():
    app = Flask(__name__)

    from onion.api.attacks.routes import attacks_blueprint
    from onion.api.classifiers.routes import classifiers_blueprint
    from onion.api.datasets.routes import datasets_blueprint

    app.register_blueprint(attacks_blueprint, url_prefix='/cv')
    app.register_blueprint(classifiers_blueprint, url_prefix='/cv')
    app.register_blueprint(datasets_blueprint, url_prefix='/cv')

    return app
