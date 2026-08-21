import os
from flask import Flask
from config import Config
from models.models import db, Project, Skill, Certificate

def create_app():
    # Set templates and static files to root '.' to match the requested folder structure
    app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints
    from routes.home import home_bp
    from routes.project import project_bp
    from routes.contact import contact_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(contact_bp)

    # Ensure database folder exists
    db_path = os.path.join(app.root_path, 'database')
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    # Seed Skills
    if Skill.query.count() == 0:
        skills = [
            Skill(name='Python / Flask / Django', category='Backend', proficiency=90),
            Skill(name='HTML5 / CSS3 / Vanilla JS', category='Frontend', proficiency=85),
            Skill(name='SQL (SQLite / PostgreSQL)', category='Database', proficiency=80),
            Skill(name='Git & Version Control', category='Tools', proficiency=85),
            Skill(name='REST APIs & JSON', category='Backend', proficiency=88),
            Skill(name='Responsive UI Design', category='Frontend', proficiency=82)
        ]
        db.session.bulk_save_objects(skills)

    # Seed Projects
    if Project.query.count() == 0:
        projects = [
            Project(
                title='E-Commerce API Service',
                description='A robust RESTful API built with Flask-SQLAlchemy, featuring authentication, shopping cart endpoints, and payment gateway integration.',
                image_url='https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&w=800&q=80',
                live_link='https://example.com/ecommerce',
                repo_link='https://github.com/sharan/ecommerce-api',
                technologies='Python, Flask, SQLite, JWT'
            ),
            Project(
                title='Personal Portfolio Platform',
                description='A modern, responsive portfolio application utilizing CSS variables, animations, and a Flask blueprint architecture to display credentials.',
                image_url='https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80',
                live_link='https://example.com/portfolio',
                repo_link='https://github.com/sharan/portfolio',
                technologies='Python, Flask, CSS3, JavaScript'
            ),
            Project(
                title='Weather Forecast Dashboard',
                description='An interactive dashboard that displays weather forecasts by connecting to third-party open APIs and caching results using SQLite.',
                image_url='https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&w=800&q=80',
                live_link='https://example.com/weather',
                repo_link='https://github.com/sharan/weather-app',
                technologies='JavaScript, Fetch API, HTML5, CSS3'
            )
        ]
        db.session.bulk_save_objects(projects)

    # Seed Certificates
    if Certificate.query.count() == 0:
        certs = [
            Certificate(
                title='Advanced Python & Flask Development',
                issuing_organization='Tech Academy',
                issue_date='June 2025',
                credential_url='https://example.com/certs/python-flask'
            ),
            Certificate(
                title='Full-Stack Software Engineering',
                issuing_organization='Global Tech Institute',
                issue_date='December 2025',
                credential_url='https://example.com/certs/fullstack'
            ),
            Certificate(
                title='Responsive Web Design Specialist',
                issuing_organization='FreeCodeCamp',
                issue_date='April 2025',
                credential_url='https://example.com/certs/responsive-design'
            )
        ]
        db.session.bulk_save_objects(certs)

    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    # Read debug from environment or default to True
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
