from datetime import datetime, timedelta, timezone
from .database import db

# UTC+8 時區
TZ_UTC8 = timezone(timedelta(hours=8))


class PingRecord(db.Model):
    """Ping 記錄模型"""
    __tablename__ = 'ping_records'
    
    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id'), nullable=False)
    ttl = db.Column(db.Integer, nullable=True)
    bytes = db.Column(db.Integer, nullable=True)
    delay_ms = db.Column(db.Float, nullable=True)
    packet_loss_percent = db.Column(db.Float, nullable=True, default=0.0)
    is_success = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """轉換為字典"""
        local_time = None
        if self.created_at:
            local_time = self.created_at.replace(tzinfo=timezone.utc).astimezone(TZ_UTC8).isoformat()
        return {
            'id': self.id,
            'target_id': self.target_id,
            'ttl': self.ttl,
            'bytes': self.bytes,
            'delay_ms': self.delay_ms,
            'packet_loss_percent': self.packet_loss_percent,
            'is_success': self.is_success,
            'error_message': self.error_message,
            'created_at': local_time
        }
    
    def __repr__(self):
        status = 'OK' if self.is_success else 'FAIL'
        return f'<PingRecord {self.target_id} {status} {self.delay_ms}ms>'
