from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Gallery, Service, Booking, Testimonial, Inquiry
from werkzeug.utils import secure_filename
import os
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── AUTH ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_bookings': Booking.query.count(),
        'pending_bookings': Booking.query.filter_by(status='pending').count(),
        'confirmed_bookings': Booking.query.filter_by(status='confirmed').count(),
        'total_inquiries': Inquiry.query.count(),
        'unread_inquiries': Inquiry.query.filter_by(read=False).count(),
        'gallery_count': Gallery.query.count(),
        'service_count': Service.query.count(),
        'testimonial_count': Testimonial.query.count(),
    }
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats,
                           recent_bookings=recent_bookings, recent_inquiries=recent_inquiries)


# ─── GALLERY ──────────────────────────────────────────────────────────────────

@admin_bp.route('/gallery')
@login_required
def gallery():
    photos = Gallery.query.order_by(Gallery.created_at.desc()).all()
    return render_template('admin/gallery.html', photos=photos)


@admin_bp.route('/gallery/upload', methods=['POST'])
@login_required
def gallery_upload():
    if 'file' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('admin.gallery'))

    file = request.files['file']
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'general').strip()
    description = request.form.get('description', '').strip()
    featured = request.form.get('featured') == 'on'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_path, exist_ok=True)
        # Make filename unique
        base, ext = os.path.splitext(filename)
        import time
        filename = f"{base}_{int(time.time())}{ext}"
        file.save(os.path.join(upload_path, filename))

        photo = Gallery(title=title or filename, category=category,
                        filename=filename, description=description, featured=featured)
        db.session.add(photo)
        db.session.commit()
        flash('Photo uploaded successfully!', 'success')
    else:
        flash('Invalid file type.', 'error')
    return redirect(url_for('admin.gallery'))


@admin_bp.route('/gallery/delete/<int:photo_id>', methods=['POST'])
@login_required
def gallery_delete(photo_id):
    photo = Gallery.query.get_or_404(photo_id)
    # Delete file from disk
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(photo)
    db.session.commit()
    flash('Photo deleted.', 'success')
    return redirect(url_for('admin.gallery'))


@admin_bp.route('/gallery/toggle-featured/<int:photo_id>', methods=['POST'])
@login_required
def gallery_toggle_featured(photo_id):
    photo = Gallery.query.get_or_404(photo_id)
    photo.featured = not photo.featured
    db.session.commit()
    return jsonify({'featured': photo.featured})


# ─── BOOKINGS ─────────────────────────────────────────────────────────────────

@admin_bp.route('/bookings')
@login_required
def bookings():
    status = request.args.get('status', 'all')
    if status == 'all':
        all_bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    else:
        all_bookings = Booking.query.filter_by(status=status).order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=all_bookings, current_status=status)


@admin_bp.route('/bookings/update-status/<int:booking_id>', methods=['POST'])
@login_required
def booking_update_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'confirmed', 'cancelled']:
        booking.status = new_status
        db.session.commit()
        flash(f'Booking status updated to {new_status}.', 'success')
    return redirect(url_for('admin.bookings'))


@admin_bp.route('/bookings/delete/<int:booking_id>', methods=['POST'])
@login_required
def booking_delete(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted.', 'success')
    return redirect(url_for('admin.bookings'))


# ─── SERVICES ─────────────────────────────────────────────────────────────────

@admin_bp.route('/services')
@login_required
def services():
    all_services = Service.query.all()
    return render_template('admin/services.html', services=all_services)


@admin_bp.route('/services/add', methods=['POST'])
@login_required
def service_add():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', 0)
    description = request.form.get('description', '').strip()
    duration = request.form.get('duration', '').strip()
    category = request.form.get('category', '').strip()
    popular = request.form.get('popular') == 'on'
    features_raw = request.form.get('features', '').strip()
    features = [f.strip() for f in features_raw.split('\n') if f.strip()]

    service = Service(name=name, price=float(price), description=description,
                      duration=duration, category=category, popular=popular)
    service.features = features
    db.session.add(service)
    db.session.commit()
    flash('Service added successfully!', 'success')
    return redirect(url_for('admin.services'))


@admin_bp.route('/services/edit/<int:service_id>', methods=['POST'])
@login_required
def service_edit(service_id):
    service = Service.query.get_or_404(service_id)
    service.name = request.form.get('name', '').strip()
    service.price = float(request.form.get('price', 0))
    service.description = request.form.get('description', '').strip()
    service.duration = request.form.get('duration', '').strip()
    service.category = request.form.get('category', '').strip()
    service.popular = request.form.get('popular') == 'on'
    features_raw = request.form.get('features', '').strip()
    service.features = [f.strip() for f in features_raw.split('\n') if f.strip()]
    db.session.commit()
    flash('Service updated!', 'success')
    return redirect(url_for('admin.services'))


@admin_bp.route('/services/delete/<int:service_id>', methods=['POST'])
@login_required
def service_delete(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted.', 'success')
    return redirect(url_for('admin.services'))


# ─── TESTIMONIALS ─────────────────────────────────────────────────────────────

@admin_bp.route('/testimonials')
@login_required
def testimonials():
    all_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=all_testimonials)


@admin_bp.route('/testimonials/add', methods=['POST'])
@login_required
def testimonial_add():
    name = request.form.get('client_name', '').strip()
    rating = int(request.form.get('rating', 5))
    review = request.form.get('review', '').strip()
    service = request.form.get('service', '').strip()
    initials = ''.join([w[0].upper() for w in name.split()[:2]])

    testimonial = Testimonial(client_name=name, rating=rating, review=review,
                              service=service, avatar_initials=initials)
    db.session.add(testimonial)
    db.session.commit()
    flash('Testimonial added!', 'success')
    return redirect(url_for('admin.testimonials'))


@admin_bp.route('/testimonials/delete/<int:tid>', methods=['POST'])
@login_required
def testimonial_delete(tid):
    t = Testimonial.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    flash('Testimonial deleted.', 'success')
    return redirect(url_for('admin.testimonials'))


# ─── INQUIRIES ────────────────────────────────────────────────────────────────

@admin_bp.route('/inquiries')
@login_required
def inquiries():
    all_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=all_inquiries)


@admin_bp.route('/inquiries/mark-read/<int:iid>', methods=['POST'])
@login_required
def inquiry_mark_read(iid):
    inquiry = Inquiry.query.get_or_404(iid)
    inquiry.read = True
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/inquiries/delete/<int:iid>', methods=['POST'])
@login_required
def inquiry_delete(iid):
    inquiry = Inquiry.query.get_or_404(iid)
    db.session.delete(inquiry)
    db.session.commit()
    flash('Inquiry deleted.', 'success')
    return redirect(url_for('admin.inquiries'))
