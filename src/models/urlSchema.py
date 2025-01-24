from app import ma
from marshmallow import validate
class UrlSchema(ma.Schema):
    id = ma.Int()
    original_url = ma.String(required = True, validate=[validate.URL()])
    short_url = ma.Int()

url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)