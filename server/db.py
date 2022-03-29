from unicodedata import category
import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db
       
    return db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def get_latest_news(limit, offset, ):
    try:
        return list(db.news.find({ }))
    except Exception as e:
        return e

def get_news_with_category(categories):
    try:
        return list(db.news.find({ "category": { "$in": categories } }).sort({ "createdAt": -1 }))
    except Exception as e:
        return e

def get_tracking_by_id(user_id):
    try:
        return db.tracking.find({ "userId": user_id })
    except Exception as e:
        return e

def create_tracking_item(user_id):
    try:
        item = { "userId": user_id, "tracking": { "business": 0, "life": 0, "sports": 0, "world": 0, "travel": 0 }, "latest": [] }
        return db.tracking.insert_one(item)
    except Exception as e:
        return e

def update_tracking_item(user_id, label):
    try:
        push = {
            "latest": {
                "$each": [label]
            }
        }
        inc = dict(zip(  ("tracking." + label), (  1 ) ))
        db.tracking.update_one({ "userId": user_id }, {  "$inc": inc, "$push": push })
    except Exception as e:
        return e
    