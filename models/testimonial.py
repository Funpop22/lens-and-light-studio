from extensions import db
from datetime import datetime

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, default=5)
    review = db.Column(db.Text, nullable=False)
    service = db.Column(db.String(100), default='')
    avatar_initials = db.Column(db.String(4), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial {self.client_name}>'
