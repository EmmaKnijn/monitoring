import os
import requests
from flask import Blueprint, render_template, current_app

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    api_url = os.getenv('API_URL', 'http://api:5000/api/v1/stats')
    api_key = os.getenv('API_KEY', 'change-me')
    headers = {'X-API-Key': api_key}
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
        stats = response.json()
    except Exception as e:
        stats = []
        print(f"Error fetching stats: {e}")
    
    # Sort stats by hostname and then timestamp
    # stats.sort(key=lambda x: (x['hostname'], x['timestamp']), reverse=True)
    
    return render_template('index.html', stats=stats)

@web_bp.route('/api_proxy/stats/<hostname>')
def proxy_stats(hostname):
    api_base_url = os.getenv('API_URL', 'http://api:5000/api/v1/stats')
    api_key = os.getenv('API_KEY', 'change-me')
    headers = {'X-API-Key': api_key}
    # api_url is http://api:5000/api/v1/stats
    # we want http://api:5000/api/v1/stats/<hostname>
    target_url = f"{api_base_url}/{hostname}"
    try:
        response = requests.get(target_url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}, 500
