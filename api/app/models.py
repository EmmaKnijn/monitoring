from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    disk_usage = db.Column(db.Float, nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    ram_usage = db.Column(db.Float, nullable=False)
    network_sent = db.Column(db.BigInteger, nullable=False)
    network_recv = db.Column(db.BigInteger, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'hostname': self.hostname,
            'timestamp': self.timestamp.isoformat(),
            'disk_usage': self.disk_usage,
            'cpu_usage': self.cpu_usage,
            'ram_usage': self.ram_usage,
            'network_sent': self.network_sent,
            'network_recv': self.network_recv
        }
