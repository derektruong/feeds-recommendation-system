from crypt import methods
from flask import Blueprint, request, jsonify
from server.db import get_latest_news

from flask_cors import CORS
from datetime import datetime

from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('./key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')

news_api_v1 = Blueprint(
    'news_api_v1', 'news_api_v1', url_prefix='/api/v1/news/')


@news_api_v1.route('/', methods=['GET'])
def generate_news():
    try:
        user_id = request.args.get('userId')
        if user_id:
            print(user_id)
            user = user_ref.document(user_id).get().to_dict()
            user_interested_fields = user["interest"]
            interest = []
            return jsonify({}), 200
        else:
            return f"An error ocurred: {e}"

    except Exception as e:
        return f"An error ocurred: {e}"
