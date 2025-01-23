from app import ma

class UrlSchema(ma.Schema):
    id = ma.Int()
    original_url = ma.String()
    short_url = ma.Int()

