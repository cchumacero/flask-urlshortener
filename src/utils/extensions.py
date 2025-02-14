from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_jwt_extended import JWTManager
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
limiter =  Limiter(
    key_func=get_remote_address,
    storage_uri= os.getenv('UPSTASH_CACHE_URL'),
    default_limits=["1000 per day", "100 per hour"] 
)
jwt = JWTManager()