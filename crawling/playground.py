from crawling.feed_crawler import Feed

categories = ["business", "travel", "sports", "life", "world"]
categories_nyt = [
    'World', 'Americas', 'AsiaPacific', 'Business', 'Africa', 'Europe',
    'EnergyEnvironment', 'SmallBusiness', 'MediaandAdvertising', 'YourMoney',
    'Economy', 'Sports', 'Soccer', 'ProFootball', 'ProBasketball', 'Golf',
    'Tennis', 'Travel', 'Arts', 'Books', 'Movies', 'Music', 'Dance',
    'Love', 'DiningandWine', 'FashionandStyle'
]

def get_news_from_vnexpress():
    news_feed = []
    feed_obj = Feed('vnexpress')
    for category in categories:
        news_feed.extend(feed_obj.fetch_from_vnexpress(category))
        
    return news_feed

def get_news_from_nyt():
    news_feed = []
    feed_obj = Feed('nyt')
    for category in categories_nyt:
        news_feed.extend(feed_obj.fetch_from_nyt(category))
        
    return news_feed