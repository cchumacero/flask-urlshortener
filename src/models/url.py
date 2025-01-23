from utils.db import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.String(100))
    short_url = db.Column(db.Integer)
    
    def __init__(self, original_url):
        self.original_url = original_url
    
    def set_short_url(self):
        self.short_url = self.id
    
    