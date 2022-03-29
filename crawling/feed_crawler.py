import feedparser
import json
import re

class Feed:
    orgs = {
        1: 'vnexpress',
        2: 'nyt',
    }
    
    def __init__(self, org):
        self.org = org
        self.url = ""
        
        if self.org == self.orgs[1]:
            self.url = "https://e.vnexpress.net/rss/"
        elif self.org == self.orgs[2]:
            self.url = "https://rss.nytimes.com/services/xml/rss/nyt/"
        
    # vnexpress
    def fetch_from_vnexpress(self, category):
        url = self.url + f"{category}.rss"
        feed = feedparser.parse(url)
        entries = feed['entries']
        formated_entries = self.lean_entries_vnexpress(entries, category)
        return formated_entries
     
    def lean_entries_vnexpress(self, entries, category):
        news = []
        for entry in entries:
            title = entry['title']
            link = entry['link']
            summary = entry['summary']
            
            imgUrl = re.findall('\<img.+src\=(?:\"|\')(.+?)(?:\"|\')(?:.+?)\>', summary)[0].replace('amp;', '')
            description = summary[summary.find('</a>') + 4 : ]
            
            news.append({
                'title': title,
                'link': link,
                'imgUrl': imgUrl,
                'description': description,
                'category': category,
            })
            
        return news
    
    # nyt
    def fetch_from_nyt(self, category):
        url = self.url + f"{category}.xml"
        feed = feedparser.parse(url)
        entries = feed['entries']
        formated_entries = self.lean_entries_nyt(entries, category)
        return formated_entries
    
    def lean_entries_nyt(self, entries, category):
        CATEGORIES = {
            'World': 'world',
            'Americas': 'world',
            'AsiaPacific': 'world',
            'Africa': 'world',
            'Europe': 'world',
            'Business': 'business',
            'EnergyEnvironment': 'business',
            'SmallBusiness': 'business',
            'Economy': 'business',
            'MediaandAdvertising': 'business',
            'YourMoney': 'business',
            'Sports': 'sports',
            'Soccer': 'sports',
            'ProFootball': 'sports',
            'ProBasketball': 'sports',
            'Golf': 'sports',
            'Tennis': 'sports',
            'Travel': 'travel',
            'Arts': 'life',
            'Books': 'life',
            'Movies': 'life',
            'Music': 'life',
            'Dance': 'life',
            'Love': 'life',
            'DiningandWine': 'life',
            'FashionandStyle': 'life',
        }
        
        news = []
        for entry in entries:
            title = entry['title']
            link = entry['link']
            description = entry['summary']
            imgUrl = ""
            if "media_content" in entry and len(entry['media_content']) > 0:
                media = entry['media_content'][0]
                imgUrl = media['url']
            
            news.append({
                'title': title,
                'link': link,
                'imgUrl': imgUrl,
                'description': description,
                'category': CATEGORIES[category],
            })
            
        return news
                
            
        