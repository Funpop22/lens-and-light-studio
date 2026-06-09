# 📸 Lens & Light Studio — Photography Website

A full-stack professional photography business website built with **Flask + SQLite** backend and a premium dark/gold glassmorphism frontend.

## ✨ Features

### Public Website
- **Home** — Hero section, featured gallery, service previews, testimonials
- **Gallery** — Filterable masonry grid (Weddings, Portraits, Family, Events, Commercial, Newborn) with lightbox
- **Services & Pricing** — Package cards with features list
- **About** — Photographer bio and stats
- **Book a Session** — Full booking form with service picker, saves to DB
- **Contact** — Contact form, saves inquiries to DB
- **Testimonials** — Client reviews with star ratings

### Admin Panel (`/admin`)
- Secure login with bcrypt password hashing
- **Dashboard** — Live stats (bookings, inquiries, gallery count)
- **Gallery Manager** — Upload, delete, and feature photos
- **Bookings** — View, confirm, cancel, delete bookings
- **Services** — Full CRUD for pricing packages
- **Testimonials** — Add and delete client reviews
- **Inquiries** — Read and reply to contact form submissions

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 + Flask |
| Database | SQLite via SQLAlchemy |
| Auth | Flask-Login + bcrypt |
| Frontend | HTML5 + Vanilla CSS + Vanilla JS |
| Fonts | Google Fonts (Playfair Display + Inter) |

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed the database (creates admin user + sample data)
```bash
python seed_db.py
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
- **Public site:** http://localhost:5000
- **Admin panel:** http://localhost:5000/admin
  - Username: `admin`
  - Password: `admin123`

> ⚠️ Change the admin password and `SECRET_KEY` in `config.py` before deploying to production.

## 📁 Project Structure

```
├── app.py                  # Flask app entry point
├── config.py               # Configuration
├── extensions.py           # Flask extensions (db, login, mail)
├── seed_db.py              # Database seeder
├── requirements.txt        # Python dependencies
├── models/                 # SQLAlchemy models
│   ├── user.py
│   ├── gallery.py
│   ├── service.py
│   ├── booking.py
│   ├── testimonial.py
│   └── inquiry.py
├── routes/
│   ├── public.py           # Public page routes
│   └── admin.py            # Admin panel routes
├── static/
│   ├── css/style.css       # Main dark/gold theme
│   ├── css/admin.css       # Admin panel styles
│   ├── js/main.js          # Animations & interactions
│   └── uploads/            # Photo uploads (not tracked by git)
└── templates/
    ├── base.html
    ├── index.html
    ├── gallery.html
    ├── services.html
    ├── about.html
    ├── booking.html
    ├── contact.html
    ├── testimonials.html
    └── admin/
        ├── login.html
        ├── dashboard.html
        ├── gallery.html
        ├── bookings.html
        ├── services.html
        ├── testimonials.html
        └── inquiries.html
```

## 📄 License

MIT License — free to use and modify.
