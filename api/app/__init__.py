import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from .models import db
from .routes import api_v1
from .swagger import swagger_blueprint, SWAGGER_URL

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Database configuration
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'system_stats')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/static/OpenAPI.yml')
    def serve_openapi():
        return send_from_directory(os.path.abspath('..'), 'OpenAPI.yml')

    return app
