import os
from flask import Flask
from config import Config
from models.models import db, Project, Skill, Certificate, Experience, User
from werkzeug.security import generate_password_hash

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
    # Seed Admin User
    if User.query.count() == 0:
        admin = User(
            username='sharan',
            email='sharanchalla5@gmail.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)

    # Seed Skills
    if Skill.query.count() == 0:
        skills = [
            Skill(name='Python & Flask', category='Backend', proficiency=95),
            Skill(name='AI & LLM Integration', category='AI/ML', proficiency=90),
            Skill(name='SQL & Relational Databases', category='Database', proficiency=88),
            Skill(name='RESTful APIs & JSON', category='Backend', proficiency=92),
            Skill(name='HTML5 / CSS3 / JavaScript', category='Frontend', proficiency=85),
            Skill(name='Git & Version Control', category='Tools', proficiency=90)
        ]
        db.session.bulk_save_objects(skills)

    # Seed Projects
    if Project.query.count() == 0:
        projects = [
            Project(
                title='AI-Native Full-Stack Platform',
                description='An intelligent web application leveraging Python, Flask, and OpenAI/Gemini LLM APIs with real-time data streaming and SQLite storage.',
                image_url='https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&w=800&q=80',
                live_link='https://www.github.com/sharanchalla',
                repo_link='https://www.github.com/sharanchalla',
                technologies='Python, Flask, LLM API, SQLite, JavaScript'
            ),
            Project(
                title='Personal Portfolio & Admin System',
                description='A modern, responsive personal website with dynamic SQL database models, custom blueprint routing, and clean UI animations.',
                image_url='https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80',
                live_link='http://127.0.0.1:5000',
                repo_link='https://www.github.com/sharanchalla',
                technologies='Python, Flask, SQLAlchemy, CSS3, JS'
            ),
            Project(
                title='Database Analytics & API Service',
                description='High-performance REST API microservice for handling dynamic database queries, user validation, and automated report generation.',
                image_url='https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&w=800&q=80',
                live_link='https://github.com/sharan',
                repo_link='https://github.com/sharan/analytics-api',
                technologies='Python, SQL, Flask, REST API'
            )
        ]
        db.session.bulk_save_objects(projects)

    # Seed Experiences
    if Experience.query.count() == 0:
        exps = [
            Experience(
                title='Python & AI-Native Full-Stack Developer',
                organization='Freelance / Tech Projects',
                period='2024 - Present',
                description='Building modern full-stack web applications, integrating AI workflows, creating Flask REST APIs, and designing responsive interfaces.',
                is_education=False
            ),
            Experience(
                title='Bachelor of Technology in Computer Science',
                organization='University Institute of Technology',
                period='2021 - 2025',
                description='Focused on Data Structures, Algorithms, Database Management Systems (SQL), Software Engineering, and Web Technologies.',
                is_education=True
            )
        ]
        db.session.bulk_save_objects(exps)

    # Seed Certificates
    if Certificate.query.count() == 0:
        certs = [
            Certificate(
                title='Python Full-Stack Development',
                issuing_organization='Tech Academy',
                issue_date='2025',
                credential_url='https://example.com/certs/python-fullstack'
            ),
            Certificate(
                title='Relational Databases & SQL Masterclass',
                issuing_organization='Global Tech Institute',
                issue_date='2025',
                credential_url='https://example.com/certs/sql-masterclass'
            )
        ]
        db.session.bulk_save_objects(certs)

    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
