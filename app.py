from flask import Flask, render_template, redirect, url_for
from config import config
from utils.extensions import db, ma, migrate, limiter, jwt, login_manager, csrf
from dotenv import load_dotenv
import os
# routes
from routes import Url, User

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    enviroment = os.environ.get('FLASK_ENV')
    
    # Configuración de la app
    app.config.from_object(config[enviroment])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRESQL_DB')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Blueprints
    app.register_blueprint(Url.main, url_prefix='/api/shorturl')
    app.register_blueprint(User.user_route, url_prefix='/api/user')
    
    @app.context_processor
    def inject_base_url():
        return dict(BASE_URL=app.config['BASE_URL'])
    
    # Errors Handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return "<h1> Not Found Page</h1>", 404
    
    @app.errorhandler(401)
    def status_401(error):
        return redirect(url_for('user_blueprint.login'))

    return app


app = create_app()
    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
