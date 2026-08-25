import os
import sys
import io
import unittest
from app import create_app
from models.models import db, Project, Skill, Certificate, Experience, User, ContactMessage, SiteProfile

class PortfolioMasterTestSuite(unittest.TestCase):
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
            'images/certificates/cisco_completion_cert.png',
            'images/certificates/cisco_data_analytics.png'
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
            profile = SiteProfile.query.first()

            self.assertIsNotNone(profile, "SiteProfile missing")
            self.assertGreaterEqual(skills_count, 10, "Skills count too low")
            self.assertGreaterEqual(projects_count, 2, "Projects missing")
            self.assertGreaterEqual(certs_count, 4, "Certificates missing")
            self.assertGreaterEqual(edu_count, 4, "Education entries missing")
            self.assertGreaterEqual(intern_count, 3, "Internship entries missing")
            self.assertIsNotNone(admin_user, "Admin user missing")
            print(f"  [OK] Database seeded: Profile '{profile.full_name}', {skills_count} Skills, {projects_count} Projects, {certs_count} Certs, {edu_count} Education, {intern_count} Internships")

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
            ('/api/profile', b'Sharan Challa'),
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
        res_unauth = self.client.get('/admin/dashboard')
        self.assertEqual(res_unauth.status_code, 302, "Unauthenticated access should redirect")

        res_login = self.client.post('/admin/login', data={
            'username': 'sharan challa',
            'password': 'sharanchalla@29'
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b'Master Site CMS & Editor', res_login.data)
        print("  [OK] Admin Login authentication successful with 'sharan challa' / 'sharanchalla@29'")

    def test_05_admin_full_site_editor_and_sync(self):
        """Test editing profile tagline, adding/deleting items and verifying static sync"""
        self.client.post('/admin/login', data={
            'username': 'sharan challa',
            'password': 'sharanchalla@29'
        })

        # 1. Update site profile tagline
        res_profile = self.client.post('/admin/profile/update', data={
            'full_name': 'Sharan Challa',
            'tagline': 'Python Developer & AI-Native Full-Stack Engineer',
            'hero_intro': 'Hi, I am',
            'about_title': 'AI-Native Full Stack Developer & Cloud Engineer',
            'about_text_p1': 'Testing bio paragraph 1',
            'about_text_p2': 'Testing bio paragraph 2',
            'email': 'sharanchalla5@gmail.com',
            'phone': '+91 86889 42778',
            'location': 'Rajahmundry, East Godavari Dist., AP, India',
            'github_url': 'https://www.github.com/sharanchalla',
            'linkedin_url': 'https://www.linkedin.com/in/sharan-challa',
            'nss_text': 'NSS Volunteer'
        }, follow_redirects=True)
        self.assertEqual(res_profile.status_code, 200)

        # Verify change in root index.html file directly on disk!
        index_disk = os.path.join(r'C:\Users\SHARAN\Downloads\portfolio', 'index.html')
        with open(index_disk, 'r', encoding='utf-8') as f:
            disk_content = f.read()
            self.assertIn('AI-Native Full-Stack Engineer', disk_content)
        print("  [OK] Profile edit synced directly to root index.html file on disk!")

        # 2. Add certificate with photo upload & verify delete
        dummy_img = (io.BytesIO(b"fake-image-bytes"), "test_cert.png")
        res_add_cert = self.client.post('/admin/certificates/add', data={
            'title': 'Test Studio Certification',
            'issuing_organization': 'AWS Cloud',
            'issue_date': '2026',
            'image_file': dummy_img
        }, follow_redirects=True)
        self.assertEqual(res_add_cert.status_code, 200)

        with self.app.app_context():
            created_cert = Certificate.query.filter_by(title='Test Studio Certification').first()
            self.assertIsNotNone(created_cert)
            cert_id = created_cert.id

            # Verify presence in disk certificates.html
            cert_disk = os.path.join(r'C:\Users\SHARAN\Downloads\portfolio', 'certificates.html')
            with open(cert_disk, 'r', encoding='utf-8') as f:
                self.assertIn('Test Studio Certification', f.read())
            print(f"  [OK] Certificate added and synced to disk (ID: {cert_id})")

            # Delete certificate
            res_del = self.client.post(f'/admin/certificates/delete/{cert_id}', follow_redirects=True)
            self.assertEqual(res_del.status_code, 200)
            
            with open(cert_disk, 'r', encoding='utf-8') as f:
                self.assertNotIn('Test Studio Certification', f.read())
            print("  [OK] Certificate deleted and immediately removed from database and disk files")

if __name__ == '__main__':
    print("===================================================")
    print("      RUNNING MASTER PORTFOLIO & CMS TEST SUITE    ")
    print("===================================================")
    suite = unittest.TestLoader().loadTestsFromTestCase(PortfolioMasterTestSuite)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
