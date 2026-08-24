from flask import Blueprint, render_template, jsonify
from models.models import Project, Skill, Certificate, Experience

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
@home_bp.route('/index.html')
def home():
    featured_projects = Project.query.order_by(Project.id.desc()).limit(3).all()
    top_skills = Skill.query.limit(6).all()
    return render_template('index.html', projects=featured_projects, skills=top_skills)

@home_bp.route('/about')
@home_bp.route('/about.html')
def about():
    educations = Experience.query.filter_by(is_education=True).all()
    return render_template('about.html', educations=educations)

@home_bp.route('/experience')
@home_bp.route('/experience.html')
def experience():
    internships = Experience.query.filter_by(is_education=False).all()
    return render_template('experience.html', internships=internships)

@home_bp.route('/skills')
@home_bp.route('/skills.html')
def skills():
    all_skills = Skill.query.all()
    categorized_skills = {}
    for skill in all_skills:
        cat = skill.category
        if cat not in categorized_skills:
            categorized_skills[cat] = []
        categorized_skills[cat].append(skill)
    return render_template('skills.html', categorized_skills=categorized_skills)

@home_bp.route('/certificates')
@home_bp.route('/certificates.html')
def certificates():
    all_certs = Certificate.query.order_by(Certificate.id.desc()).all()
    return render_template('certificates.html', certificates=all_certs)

# API Endpoints connecting Frontend AJAX to SQLite database
@home_bp.route('/api/skills')
def api_skills():
    skills = Skill.query.all()
    return jsonify([skill.to_dict() for skill in skills])

@home_bp.route('/api/certificates')
def api_certificates():
    certs = Certificate.query.all()
    return jsonify([cert.to_dict() for cert in certs])

@home_bp.route('/api/experiences')
def api_experiences():
    exps = Experience.query.all()
    return jsonify([exp.to_dict() for exp in exps])
