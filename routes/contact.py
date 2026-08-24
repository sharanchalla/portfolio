from flask import Blueprint, render_template, request, jsonify
from models.models import db, ContactMessage

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
@contact_bp.route('/contact.html', methods=['GET', 'POST'])
@contact_bp.route('/contact/submit', methods=['POST'])
def contact():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')

        if not name or not email or not subject or not message:
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        try:
            msg = ContactMessage(name=name, email=email, subject=subject, message=message)
            db.session.add(msg)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Your message has been sent successfully!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Failed to send message: {str(e)}'}), 500

    return render_template('contact.html')

@contact_bp.route('/api/contact-messages')
def get_contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([msg.to_dict() for msg in messages])
