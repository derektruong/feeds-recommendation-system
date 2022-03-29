from server.db import db

class FeedRepository(object):
    def __init__(self):
        self.db = db
        
    def find_all_by_categories(self, categories=None):
        feeds = []
        if categories is not None:
            feeds = list(self.db.feeds.find({"category": { "$in": categories } }))
        else:
            feeds = list(self.db.feeds.find({}))
        return feeds
        
    def find_many_by_categories(self, categories, skip, limit):
        return list(self.db.feeds.find({"category": { "$in": categories } }).skip(skip).limit(limit))
    
    def create_many(self, feeds):
        self.db.feeds.insert_many(feeds)