from datetime import datetime
from .database import db


class Target(db.Model):
    """監控目標模型"""
    __tablename__ = 'targets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯 ping 記錄
    ping_records = db.relationship('PingRecord', backref='target', lazy='dynamic',
                                   cascade='all, delete-orphan')
    
    def to_dict(self):
        """轉換為字典"""
        return {
            'id': self.id,
            'name': self.name,
            'ip_address': self.ip_address,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Target {self.name} ({self.ip_address})>'
