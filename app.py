import os
import uuid
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from config import Config
from models import db, AdminUser, Job, Client, GalleryPhoto, JobApplication, ContactMessage

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folders exist
os.makedirs(app.config['UPLOAD_FOLDER_GALLERY'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_CLIENTS'], exist_ok=True)

db.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_id'):
            flash('Please log in to access the administration dashboard.', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Context processor for global template variables
@app.context_processor
def inject_global_data():
    return {
        'company_name': 'JarmFabs Technologies',
        'company_tagline': 'Where Creative Charm Meets Exceptional Technology',
        'company_phone': '+91 63819 78782',
        'company_phone_clean': '916381978782',
        'company_email': 'abujabarmubarak24@gmail.com',
        'company_address': '263B Rahumaniyapuram 8th Street, Krishnapuram, Kadayanallur, Tenkasi, Tamil Nadu, India',
        'maps_url': 'https://maps.app.goo.gl/qY4frCJfDbazPDhz7',
        'linkedin_url': 'https://www.linkedin.com/company/jarmfabstechnologies/',
        'twitter_url': 'https://x.com/jarmfabstech',
        'instagram_url': 'https://www.instagram.com/jarmfabstechnologies/',
        'is_admin': bool(session.get('admin_id'))
    }

@app.template_filter('media_url')
def media_url_filter(filename, folder='gallery'):
    if not filename:
        return ''
    if filename.startswith('http://') or filename.startswith('https://'):
        return filename
    return url_for('static', filename=f'uploads/{folder}/{filename}')

def save_uploaded_file(file, folder='gallery', prefix='upload'):
    if app.config.get('CLOUDINARY_URL'):
        try:
            import cloudinary
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(
                file,
                folder=f"jarmfabs/{folder}",
                use_filename=True
            )
            return upload_result.get('secure_url')
        except Exception as e:
            app.logger.warning(f"Cloudinary upload failed, falling back to local disk: {e}")
            file.seek(0)

    ext = file.filename.rsplit('.', 1)[1].lower()
    clean_name = secure_filename(file.filename.rsplit('.', 1)[0])
    unique_name = f"{prefix}_{uuid.uuid4().hex[:8]}_{clean_name}.{ext}"
    target_folder = app.config['UPLOAD_FOLDER_GALLERY'] if folder == 'gallery' else app.config['UPLOAD_FOLDER_CLIENTS']
    save_path = os.path.join(target_folder, unique_name)
    file.save(save_path)
    return unique_name


# ==============================================================================
# FRONTEND PUBLIC ROUTES
# ==============================================================================

@app.route('/')
def index():
    clients = Client.query.order_by(Client.display_order.asc(), Client.id.asc()).limit(6).all()
    active_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(3).all()
    recent_photos = GalleryPhoto.query.order_by(GalleryPhoto.created_at.desc()).limit(6).all()
    return render_template('index.html', clients=clients, active_jobs=active_jobs, recent_photos=recent_photos)

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/industries')
def industries():
    return render_template('industries.html')

@app.route('/clients')
def clients():
    all_clients = Client.query.order_by(Client.display_order.asc(), Client.id.asc()).all()
    return render_template('clients.html', clients=all_clients)

@app.route('/innovation')
def innovation():
    return render_template('innovation.html')

@app.route('/insights')
def insights():
    return render_template('insights.html')

@app.route('/careers')
def careers():
    active_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template('careers.html', jobs=active_jobs)

@app.route('/careers/apply', methods=['POST'])
def apply_job():
    job_id = request.form.get('job_id')
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    portfolio = request.form.get('portfolio_url', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not phone:
        flash('Please fill in your name, email, and phone number.', 'error')
        return redirect(url_for('careers'))

    application = JobApplication(
        job_id=int(job_id) if job_id and job_id.isdigit() else None,
        applicant_name=name,
        email=email,
        phone=phone,
        portfolio_url=portfolio,
        message=message
    )
    db.session.add(application)
    db.session.commit()

    flash('Thank you! Your job application has been submitted successfully. Our hiring team will review it shortly.', 'success')
    return redirect(url_for('careers'))

@app.route('/gallery')
def gallery():
    selected_category = request.args.get('category', 'All')
    
    if selected_category and selected_category != 'All':
        photos = GalleryPhoto.query.filter_by(category=selected_category).order_by(GalleryPhoto.display_order.asc(), GalleryPhoto.created_at.desc()).all()
    else:
        photos = GalleryPhoto.query.order_by(GalleryPhoto.display_order.asc(), GalleryPhoto.created_at.desc()).all()

    # Get distinct available categories
    all_categories = db.session.query(GalleryPhoto.category).distinct().all()
    categories = ['All'] + [c[0] for c in all_categories if c[0]]

    return render_template('gallery.html', photos=photos, categories=categories, selected_category=selected_category)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact/submit', methods=['POST'])
def submit_contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    company = request.form.get('company', '').strip()
    service = request.form.get('service', '').strip()
    message = request.form.get('details', '').strip() or request.form.get('message', '').strip()

    if not name or not email or not message:
        flash('Please provide your name, email, and message details.', 'error')
        return redirect(url_for('contact'))

    contact_msg = ContactMessage(
        name=name,
        email=email,
        phone=phone,
        company=company,
        service=service,
        message=message
    )
    db.session.add(contact_msg)
    db.session.commit()

    flash('Thank you! Your message has been received. Our team will contact you promptly.', 'success')
    return redirect(url_for('contact'))

# ==============================================================================
# ADMIN AUTHENTICATION
# ==============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_id'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin = AdminUser.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash(f'Welcome back, {admin.username}!', 'success')
            next_url = request.args.get('next') or url_for('admin_dashboard')
            return redirect(next_url)
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

# ==============================================================================
# ADMIN DASHBOARD & MANAGEMENT
# ==============================================================================

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    jobs_count = Job.query.count()
    active_jobs_count = Job.query.filter_by(is_active=True).count()
    clients_count = Client.query.count()
    photos_count = GalleryPhoto.query.count()
    applications_count = JobApplication.query.count()
    messages_count = ContactMessage.query.count()
    
    recent_applications = JobApplication.query.order_by(JobApplication.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           jobs_count=jobs_count,
                           active_jobs_count=active_jobs_count,
                           clients_count=clients_count,
                           photos_count=photos_count,
                           applications_count=applications_count,
                           messages_count=messages_count,
                           recent_applications=recent_applications,
                           recent_messages=recent_messages)

# ---- Career / Job Management ----
@app.route('/admin/jobs')
@admin_required
def admin_jobs():
    all_jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin/jobs.html', jobs=all_jobs)

@app.route('/admin/jobs/new', methods=['GET', 'POST'])
@admin_required
def admin_job_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        department = request.form.get('department', '').strip()
        location = request.form.get('location', '').strip()
        job_type = request.form.get('job_type', 'Full-time')
        experience = request.form.get('experience', '1-3 Years')
        description = request.form.get('description', '').strip()
        requirements = request.form.get('requirements', '').strip()
        is_active = bool(request.form.get('is_active'))

        if not title or not department or not description:
            flash('Title, Department, and Description are required.', 'error')
            return render_template('admin/job_form.html', job=None)

        job = Job(
            title=title,
            department=department,
            location=location or 'Tenkasi / Hybrid',
            job_type=job_type,
            experience=experience,
            description=description,
            requirements=requirements,
            is_active=is_active
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posting created successfully!', 'success')
        return redirect(url_for('admin_jobs'))

    return render_template('admin/job_form.html', job=None)

@app.route('/admin/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_job_edit(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        job.title = request.form.get('title', '').strip()
        job.department = request.form.get('department', '').strip()
        job.location = request.form.get('location', '').strip()
        job.job_type = request.form.get('job_type', 'Full-time')
        job.experience = request.form.get('experience', '1-3 Years')
        job.description = request.form.get('description', '').strip()
        job.requirements = request.form.get('requirements', '').strip()
        job.is_active = bool(request.form.get('is_active'))

        db.session.commit()
        flash('Job posting updated successfully!', 'success')
        return redirect(url_for('admin_jobs'))

    return render_template('admin/job_form.html', job=job)

@app.route('/admin/jobs/<int:job_id>/toggle', methods=['POST'])
@admin_required
def admin_job_toggle(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    db.session.commit()
    status = 'activated' if job.is_active else 'deactivated'
    flash(f"Job '{job.title}' has been {status}.", 'info')
    return redirect(url_for('admin_jobs'))

@app.route('/admin/jobs/<int:job_id>/delete', methods=['POST'])
@admin_required
def admin_job_delete(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job posting deleted successfully.', 'info')
    return redirect(url_for('admin_jobs'))

@app.route('/admin/applications')
@admin_required
def admin_applications():
    apps = JobApplication.query.order_by(JobApplication.created_at.desc()).all()
    return render_template('admin/applications.html', applications=apps)

# ---- Client / Partner Management ----
@app.route('/admin/clients')
@admin_required
def admin_clients():
    all_clients = Client.query.order_by(Client.display_order.asc(), Client.id.asc()).all()
    return render_template('admin/clients.html', clients=all_clients)

@app.route('/admin/clients/new', methods=['GET', 'POST'])
@admin_required
def admin_client_new():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        tag = request.form.get('tag', '').strip()
        location = request.form.get('location', '').strip()
        website = request.form.get('website', '').strip()
        description = request.form.get('description', '').strip()
        display_order = int(request.form.get('display_order', 0) or 0)

        if not name or not tag:
            flash('Client Name and Industry Tag are required.', 'error')
            return render_template('admin/client_form.html', client=None)

        logo_filename = None
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename != '' and allowed_file(file.filename):
                logo_filename = save_uploaded_file(file, folder='clients', prefix='client')

        client = Client(
            name=name,
            tag=tag,
            location=location,
            website=website,
            description=description,
            logo_filename=logo_filename,
            display_order=display_order
        )
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!', 'success')
        return redirect(url_for('admin_clients'))

    return render_template('admin/client_form.html', client=None)

@app.route('/admin/clients/<int:client_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_client_edit(client_id):
    client = Client.query.get_or_404(client_id)

    if request.method == 'POST':
        client.name = request.form.get('name', '').strip()
        client.tag = request.form.get('tag', '').strip()
        client.location = request.form.get('location', '').strip()
        client.website = request.form.get('website', '').strip()
        client.description = request.form.get('description', '').strip()
        client.display_order = int(request.form.get('display_order', 0) or 0)

        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename != '' and allowed_file(file.filename):
                client.logo_filename = save_uploaded_file(file, folder='clients', prefix='client')

        db.session.commit()
        flash('Client details updated successfully!', 'success')
        return redirect(url_for('admin_clients'))

    return render_template('admin/client_form.html', client=job_client_context(client))

def job_client_context(c):
    return c

@app.route('/admin/clients/<int:client_id>/delete', methods=['POST'])
@admin_required
def admin_client_delete(client_id):
    client = Client.query.get_or_404(client_id)
    if client.logo_filename:
        logo_path = os.path.join(app.config['UPLOAD_FOLDER_CLIENTS'], client.logo_filename)
        if os.path.exists(logo_path):
            try:
                os.remove(logo_path)
            except Exception:
                pass
    db.session.delete(client)
    db.session.commit()
    flash('Client removed successfully.', 'info')
    return redirect(url_for('admin_clients'))

# ---- Photo Gallery Management ----
@app.route('/admin/gallery')
@admin_required
def admin_gallery():
    photos = GalleryPhoto.query.order_by(GalleryPhoto.created_at.desc()).all()
    return render_template('admin/gallery.html', photos=photos)

@app.route('/admin/gallery/upload', methods=['POST'])
@admin_required
def admin_gallery_upload():
    if 'photo' not in request.files:
        flash('No file was selected for upload.', 'error')
        return redirect(url_for('admin_gallery'))

    file = request.files['photo']
    if file.filename == '':
        flash('Please select an image file to upload.', 'error')
        return redirect(url_for('admin_gallery'))

    if file and allowed_file(file.filename):
        title = request.form.get('title', '').strip() or 'JarmFabs Showcase'
        category = request.form.get('category', 'Projects')
        caption = request.form.get('caption', '').strip()
        display_order = int(request.form.get('display_order', 0) or 0)

        uploaded_filename = save_uploaded_file(file, folder='gallery', prefix='gallery')

        photo = GalleryPhoto(
            title=title,
            category=category,
            caption=caption,
            filename=uploaded_filename,
            display_order=display_order
        )
        db.session.add(photo)
        db.session.commit()

        flash('Photo uploaded successfully to the gallery!', 'success')
    else:
        flash('Unsupported file type. Please upload JPG, PNG, WEBP, or GIF images.', 'error')

    return redirect(url_for('admin_gallery'))

@app.route('/admin/gallery/<int:photo_id>/delete', methods=['POST'])
@admin_required
def admin_gallery_delete(photo_id):
    photo = GalleryPhoto.query.get_or_404(photo_id)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER_GALLERY'], photo.filename)
    if os.path.exists(photo_path):
        try:
            os.remove(photo_path)
        except Exception:
            pass
    db.session.delete(photo)
    db.session.commit()
    flash('Photo removed from the gallery.', 'info')
    return redirect(url_for('admin_gallery'))

# ---- Contact Messages View ----
@app.route('/admin/messages')
@admin_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
