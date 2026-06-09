from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from extensions import db
from models import Gallery, Service, Booking, Testimonial, Inquiry
from datetime import datetime
import os

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    featured_gallery = Gallery.query.filter_by(featured=True).order_by(Gallery.created_at.desc()).limit(9).all()
    services = Service.query.limit(3).all()
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).limit(6).all()
    return render_template('index.html', featured_gallery=featured_gallery,
                           services=services, testimonials=testimonials)


@public_bp.route('/gallery')
def gallery():
    category = request.args.get('category', 'all')
    if category == 'all':
        photos = Gallery.query.order_by(Gallery.created_at.desc()).all()
    else:
        photos = Gallery.query.filter_by(category=category).order_by(Gallery.created_at.desc()).all()

    categories = db.session.query(Gallery.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template('gallery.html', photos=photos, categories=categories, current_category=category)


@public_bp.route('/services')
def services():
    all_services = Service.query.all()
    return render_template('services.html', services=all_services)


@public_bp.route('/about')
def about():
    total_bookings = Booking.query.filter_by(status='confirmed').count()
    gallery_count = Gallery.query.count()
    return render_template('about.html', total_bookings=total_bookings, gallery_count=gallery_count)


@public_bp.route('/booking', methods=['GET', 'POST'])
def booking():
    services = Service.query.all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        service_id = request.form.get('service_id')
        event_date = request.form.get('event_date', '').strip()
        event_type = request.form.get('event_type', '').strip()
        location = request.form.get('location', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, event_date]):
            flash('Please fill in all required fields.', 'error')
            return render_template('booking.html', services=services)

        booking = Booking(
            name=name, email=email, phone=phone,
            service_id=int(service_id) if service_id else None,
            event_date=event_date, event_type=event_type,
            location=location, message=message, status='pending'
        )
        db.session.add(booking)
        db.session.commit()
        flash('🎉 Your booking request has been submitted! We\'ll contact you shortly.', 'success')
        return redirect(url_for('public.booking'))

    return render_template('booking.html', services=services)


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, message]):
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html')

        inquiry = Inquiry(name=name, email=email, subject=subject, message=message)
        db.session.add(inquiry)
        db.session.commit()
        flash('✅ Your message has been sent! We\'ll get back to you within 24 hours.', 'success')
        return redirect(url_for('public.contact'))

    return render_template('contact.html')


@public_bp.route('/testimonials')
def testimonials():
    all_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('testimonials.html', testimonials=all_testimonials)


@public_bp.route('/api/gallery')
def api_gallery():
    category = request.args.get('category', 'all')
    if category == 'all':
        photos = Gallery.query.order_by(Gallery.created_at.desc()).all()
    else:
        photos = Gallery.query.filter_by(category=category).order_by(Gallery.created_at.desc()).all()

    result = [{
        'id': p.id,
        'title': p.title,
        'category': p.category,
        'filename': p.filename,
        'description': p.description
    } for p in photos]
    return jsonify(result)
