import os
from flask import render_template
from models.models import Project, Skill, Certificate, Experience, SiteProfile

def sync_all_static_files(app):
    """
    Renders all templates with the latest SQLite database state and writes
    clean static HTML versions directly to the root folder.
    This guarantees that File Explorer mode and Server mode are ALWAYS 100% in sync!
    """
    with app.app_context():
        profile = SiteProfile.query.first()
        if not profile:
            profile = SiteProfile()
            
        projects = Project.query.order_by(Project.id.desc()).all()
        skills = Skill.query.all()
        certificates = Certificate.query.order_by(Certificate.id.desc()).all()
        educations = Experience.query.filter_by(is_education=True).all()
        internships = Experience.query.filter_by(is_education=False).all()
        
        categorized_skills = {}
        for s in skills:
            cat = s.category
            if cat not in categorized_skills:
                categorized_skills[cat] = []
            categorized_skills[cat].append(s)

        pages = [
            ('index.html', {'profile': profile, 'projects': projects[:3], 'skills': skills[:6]}),
            ('about.html', {'profile': profile, 'educations': educations}),
            ('experience.html', {'profile': profile, 'internships': internships}),
            ('projects.html', {'profile': profile, 'projects': projects}),
            ('skills.html', {'profile': profile, 'categorized_skills': categorized_skills}),
            ('certificates.html', {'profile': profile, 'certificates': certificates}),
            ('contact.html', {'profile': profile})
        ]

        root_dir = app.root_path
        for template_name, context in pages:
            rendered_html = render_template(template_name, **context)
            
            # Inject instantaneous file:// bridge to top of <head>
            bridge_script = """<head>
    <script>
        if (window.location.protocol === 'file:') {
            var p = window.location.pathname.split(/[\\\\\\/]/).pop().replace('.html', '').toLowerCase();
            var target = (p === 'index' || p === '') ? '' : p;
            window.location.replace('http://127.0.0.1:5000/' + target);
        }
    </script>"""
            if '<head>' in rendered_html and 'window.location.protocol' not in rendered_html:
                rendered_html = rendered_html.replace('<head>', bridge_script, 1)
                
            out_path = os.path.join(root_dir, template_name)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
                
        print("[OK] All static HTML files in root folder synced with database!")
