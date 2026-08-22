import os
from flask import Flask
from config import Config
from models.models import db, Project, Skill, Certificate, Experience, User
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints
    from routes.home import home_bp
    from routes.project import project_bp
    from routes.contact import contact_bp
    from routes.admin import admin_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    # Ensure database folder exists
    db_path = os.path.join(app.root_path, 'database')
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    # Seed Admin User with username 'sharan challa' and password 'sharanchalla@29'
    user = User.query.filter(db.func.lower(User.username) == 'sharan challa').first()
    if not user:
        admin = User(
            username='sharan challa',
            email='sharanchalla5@gmail.com',
            password_hash=generate_password_hash('sharanchalla@29'),
            role='admin'
        )
        db.session.add(admin)

    # Seed Resume Skills
    if Skill.query.count() == 0:
        skills = [
            # Programming Languages
            Skill(name='Python', category='Programming Languages', proficiency=95),
            Skill(name='JavaScript', category='Programming Languages', proficiency=90),
            
            # AI & Machine Learning
            Skill(name='AI-Native Development', category='AI & Machine Learning', proficiency=92),
            Skill(name='Machine Learning Fundamentals', category='AI & Machine Learning', proficiency=88),
            Skill(name='Predictive Analytics', category='AI & Machine Learning', proficiency=85),

            # Web Technologies
            Skill(name='Full Stack Development', category='Web Technologies', proficiency=92),
            Skill(name='HTML5 / CSS3 / JavaScript', category='Web Technologies', proficiency=90),
            Skill(name='Flask / Python Backend', category='Web Technologies', proficiency=95),

            # Cloud & Infrastructure
            Skill(name='AWS (Amazon Web Services)', category='Cloud & Infrastructure', proficiency=88),
            Skill(name='Cloud Computing & Deployment', category='Cloud & Infrastructure', proficiency=85),

            # Developer Tools
            Skill(name='GitHub & Version Control', category='Developer Tools', proficiency=90),
            Skill(name='VS Code & Development Environments', category='Developer Tools', proficiency=92),
            Skill(name='IoT Integration', category='Developer Tools', proficiency=85),

            # Soft Skills
            Skill(name='Problem-Solving & Adaptability', category='Soft Skills', proficiency=95),
            Skill(name='Teamwork & Communication', category='Soft Skills', proficiency=92)
        ]
        db.session.bulk_save_objects(skills)

    # Seed Resume Projects
    if Project.query.count() == 0:
        projects = [
            Project(
                title='Smart Helmet System',
                description='Designed and developed an AI-powered smart helmet system to enhance rider safety and incident prevention. Implemented machine learning accident detection algorithms leveraging sensor data for real-time alerts and integrated backend APIs for data logging, predictive analytics, and emergency notifications.',
                image_url='/images/smart_helmet.jpg',
                live_link='https://www.github.com/sharanchalla',
                repo_link='https://www.github.com/sharanchalla',
                technologies='IoT, Sensor Integration, Python, AI-Based Detection, ML, REST API'
            ),
            Project(
                title='Personal Portfolio & Admin Platform',
                description='Developed a responsive portfolio application with dynamic SQL database models, session-secured admin control panel, custom Flask blueprint routing, and modern UI/UX principles for showcasing projects, skills, and resume credentials.',
                image_url='/images/portfolio_preview.png',
                live_link='http://127.0.0.1:5000',
                repo_link='https://www.github.com/sharanchalla',
                technologies='Python, Flask, SQLite, JavaScript, HTML5, CSS3'
            )
        ]
        db.session.bulk_save_objects(projects)

    # Seed Resume Experiences & Education
    if Experience.query.count() == 0:
        exps = [
            # Internships
            Experience(
                title='AI Native Full Stack Developer Intern',
                organization='Ottobon Academy (Remote)',
                period='May 2026 – July 2026',
                description='Developing AI-powered full stack applications integrating backend APIs and frontend interfaces. Working with modern web technologies and AI-assisted development workflows.',
                is_education=False
            ),
            Experience(
                title='Web Developer Intern',
                organization='Wayspire (Remote)',
                period='August 2025 – October 2025',
                description='Developed and maintained web applications using Python and modern web technologies. Collaborated with team to deploy applications using AWS infrastructure.',
                is_education=False
            ),
            Experience(
                title='Public Relations Intern',
                organization='Ascend (Remote)',
                period='January 2026 – April 2026',
                description='Led outreach efforts to media outlets and partner organizations. Coordinated with communication teams and key stakeholders to drive brand messaging and engagement.',
                is_education=False
            ),

            # Education
            Experience(
                title='B.Tech in Electronics and Communication Engineering',
                organization='GIET(A) | Rajahmundry, Andhra Pradesh',
                period='Expected Graduation: January 2027',
                description='Specializing in AI-Native Full Stack Development and Cloud Computing. Academic CGPA: 7.88 / 10.0.',
                is_education=True
            ),
            Experience(
                title='AWS DevOps Trainee Program',
                organization='TechWing | Rajahmundry, Andhra Pradesh',
                period='2024 – 2026',
                description='Hands-on training in cloud infrastructure, AWS service deployment, CI/CD workflows, and containerized application management.',
                is_education=True
            ),
            Experience(
                title='Intermediate (Class 12 - MPC)',
                organization='Vijaya Durga Junior College | Rajahmundry, AP',
                period='Completion Year: 2023',
                description='Completed Class 12 Intermediate education with an overall score of 82.9%.',
                is_education=True
            ),
            Experience(
                title='SSC (Class 10)',
                organization='Nagaraja MPL High School | Rajahmundry, AP',
                period='Completion Year: 2021',
                description='Completed Secondary School Certificate with a CGPA of 9.2 / 10.0.',
                is_education=True
            )
        ]
        db.session.bulk_save_objects(exps)

    # Seed Resume Certifications
    if Certificate.query.count() == 0:
        certs = [
            Certificate(
                title='Oracle Certified Foundations Associate',
                issuing_organization='Oracle University',
                issue_date='October 31, 2025',
                credential_url='https://education.oracle.com',
                image_url='/images/certificates/oracle_cert.png'
            ),
            Certificate(
                title='Certificate of Internship - Web Development',
                issuing_organization='Wayspire',
                issue_date='September 30, 2025',
                credential_url='https://wayspire.in',
                image_url='/images/certificates/wayspire_cert.png'
            ),
            Certificate(
                title='Networking Basics Certification',
                issuing_organization='Cisco Networking Academy',
                issue_date='March 16, 2026',
                credential_url='https://www.netacad.com',
                image_url='/images/certificates/cisco_cert.png'
            ),
            Certificate(
                title='Certificate of Course Completion - Networking Basics',
                issuing_organization='Cisco Networking Academy',
                issue_date='March 16, 2026',
                credential_url='https://www.netacad.com',
                image_url='/images/certificates/cisco_completion_cert.png'
            )
        ]
        db.session.bulk_save_objects(certs)

    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
