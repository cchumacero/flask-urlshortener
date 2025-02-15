from decouple import config

class Config:
    SECRET_KEY=config('SECRET_KEY')
    DEBUG=False
    BASE_URL='http://localhost:5000'

class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL='https://miniaturl.vercel.app'
    
class ProductionConfig(Config):
    DEBUG = False
    BASE_URL='https://miniaturl.vercel.app'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
