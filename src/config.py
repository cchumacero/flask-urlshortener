from decouple import config

class Config:
    SECRET_KEY=config('SECRET_KEY')
    DEBUG=False
    BASE_URL='http://localhost:5000'

class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL='http://localhost:5000'
    
class ProductionConfig(Config):
    DEBUG = True
    BASE_URL='http://tudominio.com'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}