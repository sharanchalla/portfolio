from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.models import db, User, Project, Skill, Certificate, Experience, ContactMessage
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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
    certificates = Certificate.query.all()
    experiences = Experience.query.all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin_dashboard.html', 
                           projects=projects, 
                           skills=skills, 
                           certificates=certificates, 
                           experiences=experiences,
                           messages=messages)

# --- SKILLS MANAGEMENT ---
@admin_bp.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    name = request.form.get('name')
    category = request.form.get('category')
    proficiency = request.form.get('proficiency', type=int)

    if name and category:
        skill = Skill(name=name, category=category, proficiency=proficiency or 85)
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/skills/delete/<int:skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# --- PROJECTS MANAGEMENT ---
@admin_bp.route('/projects/add', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    technologies = request.form.get('technologies')
    image_url = request.form.get('image_url')
    live_link = request.form.get('live_link')
    repo_link = request.form.get('repo_link')

    if title and description:
        proj = Project(
            title=title,
            description=description,
            technologies=technologies or 'Python, Full Stack',
            image_url=image_url,
            live_link=live_link,
            repo_link=repo_link
        )
        db.session.add(proj)
        db.session.commit()
        flash('Project added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    proj = Project.query.get_or_404(project_id)
    db.session.delete(proj)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# --- CERTIFICATES MANAGEMENT ---
@admin_bp.route('/certificates/add', methods=['POST'])
@login_required
def add_certificate():
    title = request.form.get('title')
    organization = request.form.get('issuing_organization')
    issue_date = request.form.get('issue_date')
    credential_url = request.form.get('credential_url')

    if title and organization:
        cert = Certificate(
            title=title,
            issuing_organization=organization,
            issue_date=issue_date or '2025',
            credential_url=credential_url
        )
        db.session.add(cert)
        db.session.commit()
        flash('Certificate added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/certificates/delete/<int:cert_id>', methods=['POST'])
@login_required
def delete_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    db.session.delete(cert)
    db.session.commit()
    flash('Certificate deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# --- EXPERIENCES / EDUCATION MANAGEMENT ---
@admin_bp.route('/experiences/add', methods=['POST'])
@login_required
def add_experience():
    title = request.form.get('title')
    organization = request.form.get('organization')
    period = request.form.get('period')
    description = request.form.get('description')
    is_education = request.form.get('is_education') == '1'

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
        flash('Education item added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/experiences/delete/<int:exp_id>', methods=['POST'])
@login_required
def delete_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    db.session.delete(exp)
    db.session.commit()
    flash('Education item deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
