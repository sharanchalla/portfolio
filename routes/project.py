from flask import Blueprint, render_template, jsonify
from models.models import db, Project, SiteProfile

project_bp = Blueprint('project', __name__)

def get_profile():
    profile = SiteProfile.query.first()
    if not profile:
        profile = SiteProfile()
        db.session.add(profile)
        db.session.commit()
    return profile

@project_bp.route('/projects')
@project_bp.route('/projects.html')
def projects():
    profile = get_profile()
    all_projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('projects.html', profile=profile, projects=all_projects)

@project_bp.route('/api/projects/<int:project_id>')
def get_project_api(project_id):
    proj = Project.query.get_or_404(project_id)
    return jsonify(proj.to_dict())
