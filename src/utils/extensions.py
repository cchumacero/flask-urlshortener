from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_limiter import Limiter
import os

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
limiter =  Limiter(
    key_func=lambda: "global",
    storage_uri= os.getenv('UPSTASH_CACHE_URL'),
    default_limits=["1000 per day", "100 per hour"] 
)