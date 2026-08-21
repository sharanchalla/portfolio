from flask import Blueprint, render_template
from models.models import Project, Skill, Certificate

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home():
    featured_projects = Project.query.limit(3).all()
    top_skills = Skill.query.limit(6).all()
    return render_template('index.html', projects=featured_projects, skills=top_skills)

@home_bp.route('/about')
def about():
    return render_template('about.html')

@home_bp.route('/skills')
def skills():
    all_skills = Skill.query.all()
    # Group skills by category
    categorized_skills = {}
    for skill in all_skills:
        cat = skill.category
        if cat not in categorized_skills:
            categorized_skills[cat] = []
        categorized_skills[cat].append(skill)
    return render_template('skills.html', categorized_skills=categorized_skills)

@home_bp.route('/certificates')
def certificates():
    all_certs = Certificate.query.all()
    return render_template('certificates.html', certificates=all_certs)
