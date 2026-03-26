from flask import Blueprint, request, jsonify
from .models import db, Stats

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/stats', methods=['GET'])
def get_stats():
    # Get the latest stats for each unique hostname
    from sqlalchemy import func
    
    # Subquery to find the latest ID for each hostname
    latest_ids = db.session.query(func.max(Stats.id)).group_by(Stats.hostname)
    
    # Fetch the stats records matching those IDs
    stats = Stats.query.filter(Stats.id.in_(latest_ids)).order_by(Stats.hostname).all()
    
    return jsonify([s.to_dict() for s in stats])

@api_v1.route('/stats/<hostname>', methods=['GET'])
def get_stats_by_hostname(hostname):
    # Fetch historical stats for a specific hostname, ordered by timestamp ascending for charting
    stats = Stats.query.filter_by(hostname=hostname).order_by(Stats.timestamp.desc()).limit(100).all()
    # Reverse to have ascending order for the chart
    return jsonify([s.to_dict() for s in reversed(stats)])

@api_v1.route('/stats', methods=['POST'])
def add_stats():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['hostname', 'disk_usage', 'cpu_usage', 'ram_usage', 'network_sent', 'network_recv']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_stat = Stats(
        hostname=data['hostname'],
        disk_usage=data['disk_usage'],
        cpu_usage=data['cpu_usage'],
        ram_usage=data['ram_usage'],
        network_sent=data['network_sent'],
        network_recv=data['network_recv']
    )
    
    db.session.add(new_stat)
    db.session.commit()
    
    return jsonify(new_stat.to_dict()), 201
