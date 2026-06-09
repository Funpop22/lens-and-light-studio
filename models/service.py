from extensions import db
import json

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, default='')
    features_json = db.Column(db.Text, default='[]')
    popular = db.Column(db.Boolean, default=False)
    duration = db.Column(db.String(50), default='')
    category = db.Column(db.String(50), default='')

    @property
    def features(self):
        return json.loads(self.features_json)

    @features.setter
    def features(self, value):
        self.features_json = json.dumps(value)

    def __repr__(self):
        return f'<Service {self.name}>'
