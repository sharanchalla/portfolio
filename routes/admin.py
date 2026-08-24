import os
import time
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from models.models import db, User, Project, Skill, Certificate, Experience, ContactMessage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif', 'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
def index():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Match exact username 'sharan challa' (case-insensitive) and password 'sharanchalla@29'
        user = User.query.filter(db.func.lower(User.username) == username.lower()).first()
        
        if user and (check_password_hash(user.password_hash, password) or password == 'sharanchalla@29'):
            session['admin_logged_in'] = True
            session['admin_user'] = user.username
            flash('Successfully logged into Admin Dashboard!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            error = 'Invalid Username or Password. Access Denied.'

    return render_template('admin_login.html', error=error)

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.order_by(Project.id.desc()).all()
    skills = Skill.query.all()
    certificates = Certificate.query.order_by(Certificate.id.desc()).all()
    educations = Experience.query.filter_by(is_education=True).all()
    internships = Experience.query.filter_by(is_education=False).all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin_dashboard.html', 
                           projects=projects, 
                           skills=skills, 
                           certificates=certificates, 
                           educations=educations,
                           internships=internships,
                           messages=messages)

# --- SKILLS MANAGEMENT ---
@admin_bp.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    proficiency = request.form.get('proficiency', type=int)

    if name and category:
        skill = Skill(name=name, category=category, proficiency=proficiency or 90)
        db.session.add(skill)
        db.session.commit()
        flash(f'Skill "{name}" added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/skills/delete/<int:skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    name = skill.name
    db.session.delete(skill)
    db.session.commit()
    flash(f'Skill "{name}" permanently removed.', 'success')
    return redirect(url_for('admin.dashboard'))

# --- PROJECTS MANAGEMENT WITH PHOTO UPLOAD ---
@admin_bp.route('/projects/add', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    technologies = request.form.get('technologies', '').strip()
    image_url = request.form.get('image_url', '').strip()
    live_link = request.form.get('live_link', '').strip()
    repo_link = request.form.get('repo_link', '').strip()

    # Handle direct photo file upload
    file = request.files.get('image_file')
    if file and file.filename != '' and allowed_file(file.filename):
        filename = f"proj_{int(time.time())}_{secure_filename(file.filename)}"
        save_dir = os.path.join(current_app.root_path, 'images')
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)
        file.save(file_path)
        image_url = f"/images/{filename}"

    if title and description:
        proj = Project(
            title=title,
            description=description,
            technologies=technologies or 'Python, Full Stack',
            image_url=image_url or '/images/portfolio_preview.png',
            live_link=live_link,
            repo_link=repo_link
        )
        db.session.add(proj)
        db.session.commit()
        flash(f'Project "{title}" added with photo!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    proj = Project.query.get_or_404(project_id)
    title = proj.title
    db.session.delete(proj)
    db.session.commit()
    flash(f'Project "{title}" permanently removed from portfolio.', 'success')
    return redirect(url_for('admin.dashboard'))

# --- CERTIFICATES MANAGEMENT WITH PHOTO UPLOAD ---
@admin_bp.route('/certificates/add', methods=['POST'])
@login_required
def add_certificate():
    title = request.form.get('title', '').strip()
    organization = request.form.get('issuing_organization', '').strip()
    issue_date = request.form.get('issue_date', '').strip()
    credential_url = request.form.get('credential_url', '').strip()
    image_url = request.form.get('image_url', '').strip()

    # Handle direct certificate image file upload
    file = request.files.get('image_file')
    if file and file.filename != '' and allowed_file(file.filename):
        filename = f"cert_{int(time.time())}_{secure_filename(file.filename)}"
        save_dir = os.path.join(current_app.root_path, 'images', 'certificates')
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)
        file.save(file_path)
        image_url = f"/images/certificates/{filename}"

    if title and organization:
        cert = Certificate(
            title=title,
            issuing_organization=organization,
            issue_date=issue_date or '2026',
            credential_url=credential_url,
            image_url=image_url or '/images/certificates/oracle_cert.png'
        )
        db.session.add(cert)
        db.session.commit()
        flash(f'Certificate "{title}" added with official image!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/certificates/delete/<int:cert_id>', methods=['POST'])
@login_required
def delete_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    title = cert.title
    db.session.delete(cert)
    db.session.commit()
    flash(f'Certificate "{title}" permanently removed.', 'success')
    return redirect(url_for('admin.dashboard'))

# --- EDUCATION & INTERNSHIP MANAGEMENT ---
@admin_bp.route('/experiences/add', methods=['POST'])
@login_required
def add_experience():
    title = request.form.get('title', '').strip()
    organization = request.form.get('organization', '').strip()
    period = request.form.get('period', '').strip()
    description = request.form.get('description', '').strip()
    entry_type = request.form.get('entry_type', 'education')
    is_education = (entry_type == 'education')

    if title and organization:
        exp = Experience(
            title=title,
            organization=organization,
            period=period or '2024 - 2026',
            description=description or '',
            is_education=is_education
        )
        db.session.add(exp)
        db.session.commit()
        kind = "Education" if is_education else "Internship"
        flash(f'{kind} entry "{title}" added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/experiences/delete/<int:exp_id>', methods=['POST'])
@login_required
def delete_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    title = exp.title
    kind = "Education" if exp.is_education else "Internship"
    db.session.delete(exp)
    db.session.commit()
    flash(f'{kind} entry "{title}" permanently removed.', 'success')
    return redirect(url_for('admin.dashboard'))

# --- CONTACT MESSAGES MANAGEMENT ---
@admin_bp.route('/messages/delete/<int:msg_id>', methods=['POST'])
@login_required
def delete_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Inquiry message permanently deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
