from flask import Blueprint, render_template, jsonify
from models.models import Project

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects')
@project_bp.route('/projects.html')
def projects():
    all_projects = Project.query.all()
    return render_template('projects.html', projects=all_projects)

@project_bp.route('/api/projects/<int:project_id>')
def get_project_api(project_id):
    proj = Project.query.get_or_404(project_id)
    return jsonify(proj.to_dict())
