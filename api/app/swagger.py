from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/v1/docs'
API_URL = '/static/OpenAPI.yml'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Knowledge Hub API"
    }
)
