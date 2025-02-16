from flask_marshmallow import Marshmallow
from marshmallow import validate, validates, ValidationError

ma = Marshmallow()

class userRegisterSchema(ma.Schema):
    id = ma.String()
    username = ma.String(required = True)
    email = ma.String(required = True, validate=[validate.Email()])
    password = ma.String(required = True)

class userLoginSchema(ma.Schema):
    csrf_token = ma.String(required = True)    
    username = ma.String(required = True)
    password = ma.String(required = True)
    
    @validates('username')
    def validate_username_or_email(self, value):
        if '@' in value:
            try:
                validate.Email()(value)
            except ValidationError:
                raise ValidationError("El email no es valido")
    
user_register_schema = userRegisterSchema()
user_login_schema = userLoginSchema()