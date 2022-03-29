from crypt import methods
from flask import Blueprint, request, jsonify
from server.db import get_tracking_by_id

from flask_cors import CORS
from datetime import datetime

from firebase_admin import credentials, firestore, initialize_app

tracking_api_v1 = Blueprint(
    'tracking_api_v1', 'tracking_api_v1', url_prefix='/api/v1/tracking')


@tracking_api_v1.route('/', methods=['POST'])
def update_tracking():
    try:
        print(request.get_json(force=True))
        return jsonify({}), 200
    except Exception as e:
        return f"An error ocurred: {e}"
