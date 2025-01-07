from flask import Flask
from config import config

# routes
from routes import Shorturl
app=Flask(__name__)

def page_not_found(error):
    return "<h1> Not Found Page</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(Shorturl.main, url_prefix='/api/shorturl')
    
    #Error handlers
    app.register_error_handler(404, page_not_found)
    app.run()


