import os
import sys
import io
import unittest
from app import create_app
from models.models import db, Project, Skill, Certificate, Experience, User, ContactMessage

class PortfolioFullTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()

    def test_01_static_assets_exist(self):
        """Verify critical CSS, JS, and image assets exist on disk"""
        assets = [
            'css/style.css',
            'css/responsive.css',
            'css/animations.css',
            'js/theme.js',
            'js/script.js',
            'images/profile_nobg.png',
            'images/portfolio_preview.png',
            'images/smart_helmet_iot.jpg',
            'images/certificates/oracle_cert.png',
            'images/certificates/wayspire_cert.png',
            'images/certificates/cisco_cert.png',
            'images/certificates/cisco_completion_cert.png'
        ]
        base_dir = r'C:\Users\SHARAN\Downloads\portfolio'
        for asset in assets:
            full_path = os.path.join(base_dir, asset)
            self.assertTrue(os.path.exists(full_path), f"Asset missing: {asset}")
            self.assertGreater(os.path.getsize(full_path), 0, f"Asset empty: {asset}")
            print(f"  [OK] Asset verified: {asset} ({os.path.getsize(full_path)} bytes)")

    def test_02_database_seeded_records(self):
        """Verify database contains all required resume models and data"""
        with self.app.app_context():
            skills_count = Skill.query.count()
            projects_count = Project.query.count()
            certs_count = Certificate.query.count()
            edu_count = Experience.query.filter_by(is_education=True).count()
            intern_count = Experience.query.filter_by(is_education=False).count()
            admin_user = User.query.filter_by(username='sharan challa').first()

            self.assertGreaterEqual(skills_count, 10, "Skills count too low")
            self.assertGreaterEqual(projects_count, 2, "Projects missing")
            self.assertGreaterEqual(certs_count, 4, "Certificates missing")
            self.assertGreaterEqual(edu_count, 4, "Education entries missing")
            self.assertGreaterEqual(intern_count, 3, "Internship entries missing")
            self.assertIsNotNone(admin_user, "Admin user missing")
            print(f"  [OK] Database seeded: {skills_count} Skills, {projects_count} Projects, {certs_count} Certs, {edu_count} Education, {intern_count} Internships, Admin User found")

    def test_03_all_public_get_routes(self):
        """Test HTTP 200 on all public frontend web routes"""
        routes = [
            ('/', b'Sharan Challa'),
            ('/about', b'About Me & Education'),
            ('/experience', b'Internships & Experience'),
            ('/projects', b'My Projects'),
            ('/skills', b'Technical Skills'),
            ('/certificates', b'Licenses & Certifications'),
            ('/contact', b'Get in Touch'),
            ('/api/skills', b'Python'),
            ('/api/certificates', b'Oracle'),
            ('/api/experiences', b'Ottobon')
        ]
        for route, expected_text in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} returned status {response.status_code}")
            self.assertIn(expected_text, response.data, f"Expected text not found in {route}")
            print(f"  [OK] GET {route} -> 200 OK (Verified content)")

    def test_04_admin_login_and_auth(self):
        """Test Admin login authentication flow and session protection"""
        # 1. Access dashboard without login -> redirect to login
        res_unauth = self.client.get('/admin/dashboard')
        self.assertEqual(res_unauth.status_code, 302, "Unauthenticated access should redirect")

        # 2. Login with correct credentials
        res_login = self.client.post('/admin/login', data={
            'username': 'sharan challa',
            'password': 'sharanchalla@29'
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b'Admin Manager & CMS', res_login.data)
        print("  [OK] Admin Login authentication successful with 'sharan challa' / 'sharanchalla@29'")

    def test_05_admin_photo_upload_and_permanent_delete(self):
        """Test adding a certificate with an image file and deleting permanently"""
        # Login first
        self.client.post('/admin/login', data={
            'username': 'sharan challa',
            'password': 'sharanchalla@29'
        })

        # 1. Add new certificate with direct photo upload
        dummy_img = (io.BytesIO(b"fake-image-bytes"), "test_cert.png")
        res_add_cert = self.client.post('/admin/certificates/add', data={
            'title': 'Test Cloud Certification',
            'issuing_organization': 'AWS Academy',
            'issue_date': '2026',
            'image_file': dummy_img
        }, follow_redirects=True)
        self.assertEqual(res_add_cert.status_code, 200)

        with self.app.app_context():
            created_cert = Certificate.query.filter_by(title='Test Cloud Certification').first()
            self.assertIsNotNone(created_cert, "Certificate with photo upload was not created")
            self.assertTrue(created_cert.image_url.startswith('/images/certificates/cert_'), "Image URL not generated properly")
            cert_id = created_cert.id
            print(f"  [OK] Certificate with uploaded photo created successfully (ID: {cert_id}, URL: {created_cert.image_url})")

            # 2. Permanently delete the certificate
            res_del_cert = self.client.post(f'/admin/certificates/delete/{cert_id}', follow_redirects=True)
            self.assertEqual(res_del_cert.status_code, 200)
            deleted_cert = Certificate.query.get(cert_id)
            self.assertIsNone(deleted_cert, "Certificate was not permanently removed from database")
            print("  [OK] Certificate permanently removed from SQLite database")

    def test_06_contact_form_submission_and_deletion(self):
        """Test submitting a contact message and deleting it in admin"""
        res_contact = self.client.post('/contact/submit', data={
            'name': 'Test Recruiter',
            'email': 'recruiter@techcompany.com',
            'subject': 'Job Opportunity',
            'message': 'Hello Sharan, we would love to connect with you regarding a Full Stack AI role.'
        }, follow_redirects=True)
        self.assertEqual(res_contact.status_code, 200)

        with self.app.app_context():
            msg = ContactMessage.query.filter_by(email='recruiter@techcompany.com').first()
            self.assertIsNotNone(msg, "Contact message not saved to database")
            msg_id = msg.id
            print("  [OK] Contact form submission stored successfully in SQLite database")

            # Delete message via admin
            res_del_msg = self.client.post(f'/admin/messages/delete/{msg_id}', follow_redirects=True)
            self.assertEqual(res_del_msg.status_code, 200)
            deleted_msg = ContactMessage.query.get(msg_id)
            self.assertIsNone(deleted_msg, "Message was not permanently deleted")
            print("  [OK] Contact message permanently deleted via Admin Portal")

if __name__ == '__main__':
    print("===================================================")
    print("      RUNNING FULL SHARAN CHALLA PORTFOLIO TEST    ")
    print("===================================================")
    suite = unittest.TestLoader().loadTestsFromTestCase(PortfolioFullTestSuite)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
