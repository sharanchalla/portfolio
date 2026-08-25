from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SiteProfile(db.Model):
    __tablename__ = 'site_profile'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), default='Sharan Challa')
    tagline = db.Column(db.String(150), default='Python Developer & AI-Native Full-Stack Developer')
    hero_intro = db.Column(db.String(50), default='Hi, I am')
    about_title = db.Column(db.String(150), default='AI-Native Full Stack Developer & Cloud Engineer')
    about_text_p1 = db.Column(db.Text, default='Final-year Electronics and Communication Engineering (ECE) student at GIET(A), Rajahmundry with expertise in AI-Native Full Stack Development and Cloud Computing. Hands-on experience building AI-powered applications, smart IoT systems, and deploying scalable solutions on AWS.')
    about_text_p2 = db.Column(db.Text, default='Passionate about problem-solving, clean software architecture, and intelligent web applications. Active NSS Volunteer contributing to sustainable community development initiatives and environmental conservation.')
    profile_photo = db.Column(db.String(255), default='images/profile_nobg.png')
    email = db.Column(db.String(100), default='sharanchalla5@gmail.com')
    phone = db.Column(db.String(50), default='+91 86889 42778')
    location = db.Column(db.String(150), default='Rajahmundry, East Godavari Dist., AP, India')
    github_url = db.Column(db.String(255), default='https://www.github.com/sharanchalla')
    linkedin_url = db.Column(db.String(255), default='https://www.linkedin.com/in/sharan-challa')
    nss_text = db.Column(db.Text, default='Actively participated in agricultural programs, drainage system survey initiatives, and sustainable community development projects.')

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'tagline': self.tagline,
            'hero_intro': self.hero_intro,
            'about_title': self.about_title,
            'about_text_p1': self.about_text_p1,
            'about_text_p2': self.about_text_p2,
            'profile_photo': self.profile_photo,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'github_url': self.github_url,
            'linkedin_url': self.linkedin_url,
            'nss_text': self.nss_text
        }

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    live_link = db.Column(db.String(255), nullable=True)
    repo_link = db.Column(db.String(255), nullable=True)
    technologies = db.Column(db.String(255), nullable=False)  # Comma-separated list
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'live_link': self.live_link,
            'repo_link': self.repo_link,
            'technologies': [tech.strip() for tech in self.technologies.split(',') if tech.strip()],
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., Backend, Frontend, AI/ML, Tools
    proficiency = db.Column(db.Integer, nullable=False)  # 0 to 100

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'proficiency': self.proficiency
        }

class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    issuing_organization = db.Column(db.String(100), nullable=False)
    issue_date = db.Column(db.String(50), nullable=False)
    credential_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'issuing_organization': self.issuing_organization,
            'issue_date': self.issue_date,
            'credential_url': self.credential_url,
            'image_url': self.image_url
        }

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_education = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'organization': self.organization,
            'period': self.period,
            'description': self.description,
            'is_education': self.is_education
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
