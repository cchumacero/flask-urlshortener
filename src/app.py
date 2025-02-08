from flask import Flask
from config import config
from utils.db import db
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from flask_limiter import Limiter
import os

# routes
from routes import Url

load_dotenv()
app = Flask(__name__)
ma = Marshmallow(app)

limiter =  Limiter(
    key_func=lambda: "global",
    app=app,
    storage_uri= os.getenv('UPSTASH_CACHE_URL'),
    default_limits=["1000 per day", "100 per hour"] 
)

def page_not_found(error):
    return "<h1> Not Found Page</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRESQL_DB')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    # Blueprints
    app.register_blueprint(Url.main, url_prefix='/api/shorturl')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run()
