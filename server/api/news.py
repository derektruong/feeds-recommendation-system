import json
import random
import math
from crypt import methods
from flask import Blueprint, request, jsonify

from flask_cors import CORS
from datetime import datetime

from server.api.utils import MongoJsonEncoder
from server.repository.feedRepository import FeedRepository

from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('./key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')


# repository
feedRepository = FeedRepository()

news_api_v1 = Blueprint(
    'news_api_v1', 'news_api_v1', url_prefix='/api/v1/news/'
)

@news_api_v1.route('/', methods=['GET'])
def generate_news():
    try:
        user_id = request.args.get('userId')
        if user_id:
            user = user_ref.document(user_id).get().to_dict()
            user_interested_fields = user["interest"]
            leanFeeds = []
            if user_interested_fields is not None and len(user_interested_fields) != 0:
                feeds = feedRepository.find_all_by_categories(user_interested_fields)
                random.shuffle(feeds)
                leanFeeds = list(map(lambda feed: json.loads(MongoJsonEncoder().encode(feed)), feeds[:30]))
            else:
                favorite_tags = user["favorites"]
                print(favorite_tags)
                
                sorted_tags = {k: v for k, v in sorted(favorite_tags.items(), key=lambda item: item[1], reverse=True) if v != 0}
                total_score = sum(sorted_tags.values())
                if total_score > 0:
                    feeds = []
                    weight = 30 / total_score
                    for k, v in sorted_tags.items():
                        feeds.extend(feedRepository.find_many_by_categories([k], 0, math.ceil(weight * v)))
                    random.shuffle(leanFeeds)
                    leanFeeds = list(map(lambda feed: json.loads(MongoJsonEncoder().encode(feed)), feeds))
                else:
                    feeds = feedRepository.find_all_by_categories()
                    random.shuffle(feeds)
                    leanFeeds = list(map(lambda feed: json.loads(MongoJsonEncoder().encode(feed)), feeds[:30]))
            return {
                'feeds': leanFeeds,
            }, 200

        else:
            return f"An error ocurred"

    except Exception as e:
        return f"An error ocurred: {e}"
    
@news_api_v1.route('/feeds', methods=['POST'])
def store_feeds():
    try:
        feeds = request.json.get('data')
        feedRepository.create_many(feeds)
        return {
            'success': "true",
        }
    except Exception as e:
        return f"An error ocurred"
