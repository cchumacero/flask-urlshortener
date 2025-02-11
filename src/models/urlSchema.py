from flask_marshmallow import Marshmallow
from marshmallow import validate

ma = Marshmallow()

class UrlSchema(ma.Schema):
    id = ma.Int()
    original_url = ma.String(required = True, validate=[validate.URL()])
    short_url = ma.String()

url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)