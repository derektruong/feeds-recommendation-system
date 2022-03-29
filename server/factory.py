import os

from flask import Flask, render_template
from flask_cors import CORS
##from flask_bcrypt import Bcrypt
##from flask_jwt_extended import JWTManager

from server.api.news import news_api_v1
from server.api.tracking import tracking_api_v1

def create_app():
    app = Flask(__name__)
    app.register_blueprint(news_api_v1)
    app.register_blueprint(tracking_api_v1)
    return app