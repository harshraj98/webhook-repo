from flask import Flask

from app.webhook.routes import webhook


# Creating our flask app
def create_app():
    app = Flask(__name__)
    app.register_blueprint(webhook)

    return app
