try:
    # Local execution from the api directory (python main.py)
    from app import create_app
except ModuleNotFoundError:
    # Package-style import used by Azure startup (gunicorn api.main:app)
    from api.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
