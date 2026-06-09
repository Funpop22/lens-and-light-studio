from flask import Flask
from config import Config
from extensions import db, login_manager, mail
from models import User
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload and database directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access the admin panel.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.public import public_bp
    from routes.admin import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # Create all tables and seed if empty
    with app.app_context():
        db.create_all()
        # Auto-seed on first run (production)
        _auto_seed(app)

    return app


def _auto_seed(app):
    """Seed default admin + services + testimonials if DB is empty."""
    from models import User, Service, Testimonial
    import json

    with app.app_context():
        # Admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@lensandlight.com')
            admin.set_password('admin123')
            db.session.add(admin)

        # Services
        if Service.query.count() == 0:
            services = [
                {'name': 'Portrait Session',  'price': 199,  'duration': '2 Hours',    'category': 'Portrait',    'popular': False,
                 'description': 'A personalised portrait session capturing your unique personality.',
                 'features': ['2-hour session', '50+ edited photos', 'Online gallery delivery', '1 location', 'Print-ready files']},
                {'name': 'Wedding Package',   'price': 1499, 'duration': 'Full Day',   'category': 'Wedding',     'popular': True,
                 'description': 'Full-day wedding coverage telling the complete story of your special day.',
                 'features': ['Full-day coverage (10 hrs)', '600+ edited photos', '2 photographers', 'Engagement session', 'Premium album']},
                {'name': 'Event Photography', 'price': 499,  'duration': '4 Hours',    'category': 'Events',      'popular': False,
                 'description': 'Professional coverage for corporate events, parties and galas.',
                 'features': ['4-hour coverage', '200+ edited photos', 'Online gallery', 'Commercial license', 'Same-week delivery']},
                {'name': 'Family Session',    'price': 299,  'duration': '3 Hours',    'category': 'Family',      'popular': False,
                 'description': 'Warm and natural family portraits preserving your cherished moments.',
                 'features': ['3-hour session', '100+ edited photos', 'Multiple locations', 'All family members', 'Print-ready files']},
                {'name': 'Commercial Shoot',  'price': 799,  'duration': 'Half Day',   'category': 'Commercial',  'popular': False,
                 'description': 'Professional product and brand photography for your marketing materials.',
                 'features': ['Half-day session', '80+ edited photos', 'Commercial license', 'Concept planning', 'RAW files included']},
                {'name': 'Newborn Session',   'price': 349,  'duration': '3-4 Hours',  'category': 'Newborn',     'popular': False,
                 'description': 'Gentle newborn photography capturing the miracle of new life.',
                 'features': ['3-4 hour session', '60+ edited photos', 'Prop styling included', 'Safe posing expertise', 'Print-ready files']},
            ]
            for s in services:
                svc = Service(name=s['name'], price=s['price'], description=s['description'],
                              duration=s['duration'], category=s['category'], popular=s['popular'])
                svc.features = s['features']
                db.session.add(svc)

        # Testimonials
        if Testimonial.query.count() == 0:
            testimonials = [
                {'client_name': 'Sarah & James Mitchell', 'rating': 5, 'service': 'Wedding Package',
                 'review': 'Absolutely breathtaking! Our wedding photos exceeded every expectation. Every family member has commented on how beautiful the photos are.'},
                {'client_name': 'Emily Rodriguez', 'rating': 5, 'service': 'Portrait Session',
                 'review': 'I was so nervous but you made me feel completely at ease. The results are stunning — I have never felt so confident in photos before!'},
                {'client_name': 'The Johnson Family', 'rating': 5, 'service': 'Family Session',
                 'review': 'Our family session was an absolute joy. You have a magical ability to capture genuine moments with three kids. The photos are now displayed throughout our home.'},
                {'client_name': 'Bloom Cosmetics', 'rating': 5, 'service': 'Commercial Shoot',
                 'review': 'Our product campaign was elevated to a new level. Sales increased 40% after we updated our marketing with these images.'},
                {'client_name': 'TechCorp Solutions', 'rating': 5, 'service': 'Event Photography',
                 'review': 'Professional, punctual, and the photos perfectly captured our company culture. Highly recommend for any corporate event.'},
                {'client_name': 'Amanda & Tom Parker', 'rating': 5, 'service': 'Newborn Session',
                 'review': "From the moment you arrived, you put us completely at ease. Our baby's photos are absolutely magical."},
            ]
            for t in testimonials:
                initials = ''.join([w[0].upper() for w in t['client_name'].split()[:2]])
                db.session.add(Testimonial(client_name=t['client_name'], rating=t['rating'],
                                           review=t['review'], service=t['service'], avatar_initials=initials))

        db.session.commit()



app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
