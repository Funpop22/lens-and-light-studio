"""
Script to replace placeholder gallery entries with real generated images.
Run once: python update_gallery.py
"""
from app import app
from extensions import db
from models.gallery import Gallery

PHOTOS = [
    # Weddings
    dict(title='Golden Hour Ceremony',       category='weddings',  filename='wedding_golden_hour_1780482888174.png',      featured=True,  description='Bride and groom under a floral arch at golden hour'),
    dict(title='Bride Portrait',              category='weddings',  filename='wedding_bride_portrait_1780482901835.png',    featured=True,  description='Elegant close-up bridal portrait with soft natural light'),
    dict(title='First Dance',                 category='weddings',  filename='wedding_reception_dance_1780482977658.png',   featured=True,  description='Romantic first dance with fairy light bokeh'),
    # Portraits
    dict(title='Dramatic Studio Portrait',    category='portraits', filename='portrait_studio_dramatic_1780482915287.png',  featured=True,  description='Rembrandt-lit studio portrait'),
    dict(title='Golden Hour Portrait',        category='portraits', filename='portrait_outdoor_golden_1780482929563.png',   featured=False, description='Outdoor backlit portrait at golden hour'),
    dict(title='Professional Headshot',       category='portraits', filename='portrait_headshot_professional_1780483027688.png', featured=False, description='Clean corporate headshot'),
    # Family
    dict(title='Autumn Family Session',       category='family',    filename='family_autumn_park_1780482943061.png',        featured=True,  description='Candid family laughter in an autumn park'),
    dict(title='Beach Sunset Family',         category='family',    filename='family_beach_sunset_1780483017180.png',       featured=False, description='Silhouette of a family at sunset on the beach'),
    # Newborn
    dict(title='Newborn Serenity',            category='newborn',   filename='newborn_sleeping_baby_1780482957068.png',     featured=True,  description='Peacefully sleeping newborn in soft white wrap'),
    # Events
    dict(title='Corporate Gala Evening',      category='events',    filename='event_corporate_gala_1780482991536.png',      featured=False, description='Elegant corporate gala with chandeliers'),
    dict(title='Birthday Celebration',        category='events',    filename='event_birthday_celebration_1780483042444.png',featured=False, description='Joyful birthday party candid shots'),
    # Commercial
    dict(title='Luxury Product Shoot',        category='commercial',filename='commercial_product_cosmetics_1780483004643.png',featured=False,description='High-end perfume product photography'),
]

def update():
    with app.app_context():
        # Remove old placeholder entries (filenames starting with 'placeholder_')
        old = Gallery.query.filter(Gallery.filename.like('placeholder_%')).all()
        for o in old:
            db.session.delete(o)
        print(f"Removed {len(old)} placeholder entries")

        # Add real photo entries (skip if already inserted)
        added = 0
        for p in PHOTOS:
            exists = Gallery.query.filter_by(filename=p['filename']).first()
            if not exists:
                db.session.add(Gallery(**p))
                added += 1

        db.session.commit()
        print(f"Added {added} real photo entries")
        print(f"Total gallery photos: {Gallery.query.count()}")
        print("Done! Visit http://localhost:5000/gallery")

if __name__ == '__main__':
    update()
