from app import app
from extensions import db
from models import User, Gallery, Service, Booking, Testimonial, Inquiry
import json

def seed():
    with app.app_context():
        db.create_all()

        # -- Admin User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@lensandlight.com')
            admin.set_password(os.environ.get('ADMIN_PASSWORD','admin123'))
            db.session.add(admin)
            print("[OK] Admin user created -> username: admin")

        # -- Services
        if Service.query.count() == 0:
            services = [
                {
                    'name': 'Portrait Session',
                    'price': 199,
                    'description': 'A personalized portrait session capturing your unique personality with professional lighting and creative compositions.',
                    'duration': '2 Hours',
                    'category': 'Portrait',
                    'popular': False,
                    'features': ['2-hour session', '50+ edited photos', 'Online gallery delivery', '1 location', 'Personal styling tips', 'Print-ready files']
                },
                {
                    'name': 'Wedding Package',
                    'price': 1499,
                    'description': 'Full-day wedding coverage that tells the complete story of your most special day with cinematic imagery.',
                    'duration': 'Full Day',
                    'category': 'Wedding',
                    'popular': True,
                    'features': ['Full-day coverage (10 hrs)', '600+ edited photos', 'Online gallery', '2 photographers', 'Engagement session', 'Premium photo album', 'Rush delivery option']
                },
                {
                    'name': 'Event Photography',
                    'price': 499,
                    'description': 'Professional coverage for corporate events, parties, galas, and special occasions.',
                    'duration': '4 Hours',
                    'category': 'Events',
                    'popular': False,
                    'features': ['4-hour coverage', '200+ edited photos', 'Online gallery', 'Commercial license', 'Same-week delivery', 'Print-ready files']
                },
                {
                    'name': 'Family Session',
                    'price': 299,
                    'description': 'Warm and natural family portraits that preserve your most cherished moments together.',
                    'duration': '3 Hours',
                    'category': 'Family',
                    'popular': False,
                    'features': ['3-hour session', '100+ edited photos', 'Multiple locations', 'All family members', 'Online gallery', 'Print-ready files']
                },
                {
                    'name': 'Commercial Shoot',
                    'price': 799,
                    'description': 'Professional product and brand photography designed to elevate your marketing materials.',
                    'duration': 'Half Day',
                    'category': 'Commercial',
                    'popular': False,
                    'features': ['Half-day session', '80+ edited photos', 'Commercial license', 'Concept planning', 'Multiple setups', 'RAW files included']
                },
                {
                    'name': 'Newborn Session',
                    'price': 349,
                    'description': 'Gentle and safe newborn photography capturing the miracle of new life in artistic portraits.',
                    'duration': '3-4 Hours',
                    'category': 'Newborn',
                    'popular': False,
                    'features': ['3-4 hour session', '60+ edited photos', 'Prop styling included', 'Safe posing expertise', 'Online gallery', 'Print-ready files']
                },
            ]
            for s in services:
                svc = Service(name=s['name'], price=s['price'], description=s['description'],
                              duration=s['duration'], category=s['category'], popular=s['popular'])
                svc.features = s['features']
                db.session.add(svc)
            print("[OK] 6 services seeded")

        # ── Testimonials ──────────────────────────────────────────
        if Testimonial.query.count() == 0:
            testimonials = [
                {'client_name': 'Sarah & James Mitchell', 'rating': 5, 'review': 'Absolutely breathtaking! Our wedding photos exceeded every expectation. The way you captured the emotions of our day is something we will treasure forever. Every family member has commented on how beautiful the photos are.', 'service': 'Wedding Package'},
                {'client_name': 'Emily Rodriguez', 'rating': 5, 'review': 'I was so nervous for my portrait session but you made me feel completely at ease. The results are stunning — I\'ve never felt so confident in photos before. Will definitely be back for future sessions!', 'service': 'Portrait Session'},
                {'client_name': 'TechCorp Solutions', 'rating': 5, 'review': 'We hired for our annual company gala and could not be happier with the results. Professional, punctual, and the photos perfectly captured our company culture. Highly recommend for any corporate event.', 'service': 'Event Photography'},
                {'client_name': 'The Johnson Family', 'rating': 5, 'review': 'Our family session was an absolute joy from start to finish. You have a magical ability to capture genuine moments with three kids — no small feat! The photos are now proudly displayed throughout our home.', 'service': 'Family Session'},
                {'client_name': 'Bloom Cosmetics', 'rating': 5, 'review': 'Our product campaign photography was elevated to a completely new level. The creative direction and technical expertise brought our brand vision to life perfectly. Sales increased 40% after we updated our marketing with these images.', 'service': 'Commercial Shoot'},
                {'client_name': 'Amanda & Tom Parker', 'rating': 5, 'review': 'We were so worried about getting a newborn photographer but from the moment you arrived, you put us completely at ease. Our baby\'s photos are absolutely magical. Thank you for such a wonderful experience.', 'service': 'Newborn Session'},
            ]
            for t in testimonials:
                initials = ''.join([w[0].upper() for w in t['client_name'].split()[:2]])
                testimonial = Testimonial(client_name=t['client_name'], rating=t['rating'],
                                          review=t['review'], service=t['service'], avatar_initials=initials)
                db.session.add(testimonial)
            print("[OK] 6 testimonials seeded")

        # ── Gallery Placeholders ──────────────────────────────────
        if Gallery.query.count() == 0:
            gallery_items = [
                {'title': 'Golden Hour Wedding', 'category': 'weddings', 'filename': 'placeholder_wedding1.jpg', 'featured': True},
                {'title': 'Bride & Groom Portrait', 'category': 'weddings', 'filename': 'placeholder_wedding2.jpg', 'featured': True},
                {'title': 'Romantic Sunset Kiss', 'category': 'weddings', 'filename': 'placeholder_wedding3.jpg', 'featured': False},
                {'title': 'Studio Portrait', 'category': 'portraits', 'filename': 'placeholder_portrait1.jpg', 'featured': True},
                {'title': 'Outdoor Portrait', 'category': 'portraits', 'filename': 'placeholder_portrait2.jpg', 'featured': False},
                {'title': 'Corporate Headshot', 'category': 'portraits', 'filename': 'placeholder_portrait3.jpg', 'featured': False},
                {'title': 'Family in the Park', 'category': 'family', 'filename': 'placeholder_family1.jpg', 'featured': True},
                {'title': 'Newborn Session', 'category': 'newborn', 'filename': 'placeholder_newborn1.jpg', 'featured': True},
                {'title': 'Corporate Gala', 'category': 'events', 'filename': 'placeholder_event1.jpg', 'featured': False},
                {'title': 'Product Campaign', 'category': 'commercial', 'filename': 'placeholder_commercial1.jpg', 'featured': False},
            ]
            for g in gallery_items:
                photo = Gallery(title=g['title'], category=g['category'],
                                filename=g['filename'], featured=g['featured'])
                db.session.add(photo)
            print("[OK] 10 gallery placeholder entries seeded")

        db.session.commit()
        print("\n[DONE] Database seeded successfully!")
        print("   Admin URL:  http://localhost:5000/admin")
        print("   Public URL: http://localhost:5000/")

if __name__ == '__main__':
    seed()
