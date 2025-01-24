from utils.db import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.String(100))
    short_url = db.Column(db.String(8))
    
    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url
    
    