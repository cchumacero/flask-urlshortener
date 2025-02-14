from utils.extensions import db
from datetime import datetime
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.String(100), nullable = False)
    short_url = db.Column(db.String(8), unique=True, nullable = False)
    user_id = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    clicks = db.Column(db.Integer, default=0)
    
    def __init__(self, original_url, short_url, user_id):
        self.original_url = original_url
        self.short_url = short_url
        self.user_id = user_id
    
    def count_click(self):
        self.clicks = self.clicks + 1
    