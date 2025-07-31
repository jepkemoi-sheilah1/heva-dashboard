from flask import Blueprint, request, jsonify, abort
from app.models import db, User, Platform, Message, FAQ, Analytics, Settings
from app.services import fetch_data_from_open_source_api

from flask import Blueprint, request, jsonify, abort, send_from_directory
from app.models import db, User, Platform, Message, FAQ, Analytics, Settings
from app.services import fetch_data_from_open_source_api
import os

main = Blueprint('main', __name__)

# Serve frontend index.html at root to fix 404 on /
@main.route('/', methods=['GET'])
def serve_index():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))
    return send_from_directory(frontend_path, 'index.html')

# Serve static files like main.css and main.js
@main.route('/<path:filename>')
def serve_static_files(filename):
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))
    return send_from_directory(frontend_path, filename)

# User routes
@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email, 'role': u.role} for u in users])

@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role})

# Platform routes
@main.route('/platforms', methods=['GET'])
def get_platforms():
    platforms = Platform.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'icon_url': p.icon_url, 'is_active': p.is_active} for p in platforms])

@main.route('/platforms/<int:platform_id>', methods=['GET'])
def get_platform(platform_id):
    platform = Platform.query.get_or_404(platform_id)
    return jsonify({'id': platform.id, 'name': platform.name, 'icon_url': platform.icon_url, 'is_active': platform.is_active})

# Message routes
@main.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{'id': m.id, 'content': m.content, 'timestamp': m.timestamp.isoformat(), 'direction': m.direction,
                     'user_id': m.user_id, 'platform_id': m.platform_id} for m in messages])

@main.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'content' not in data or 'direction' not in data or 'user_id' not in data or 'platform_id' not in data:
        abort(400, description="Missing required fields")
    message = Message()
    message.content = data['content']
    message.direction = data['direction']
    message.user_id = data['user_id']
    message.platform_id = data['platform_id']
    db.session.add(message)
    db.session.commit()
    return jsonify({'message': 'Message sent', 'id': message.id}), 201

# FAQ routes
@main.route('/faqs', methods=['GET'])
def get_faqs():
    faqs = FAQ.query.all()
    return jsonify([{'id': f.id, 'question': f.question, 'answer': f.answer, 'category': f.category, 'times_asked': f.times_asked} for f in faqs])

@main.route('/faqs', methods=['POST'])
def add_faq():
    data = request.get_json()
    if not data or 'question' not in data:
        abort(400, description="Missing question field")
    faq = FAQ()
    faq.question = data['question']
    faq.answer = data.get('answer')
    faq.category = data.get('category')
    db.session.add(faq)
    db.session.commit()
    return jsonify({'message': 'FAQ added', 'id': faq.id}), 201

@main.route('/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    faq = FAQ.query.get_or_404(faq_id)
    data = request.get_json()
    if not data:
        abort(400, description="Missing data")
    faq.question = data.get('question', faq.question)
    faq.answer = data.get('answer', faq.answer)
    faq.category = data.get('category', faq.category)
    faq.times_asked = data.get('times_asked', faq.times_asked)
    db.session.commit()
    return jsonify({'message': 'FAQ updated'})

# Analytics routes
@main.route('/analytics', methods=['GET'])
def get_analytics():
    analytics = Analytics.query.all()
    return jsonify([{'id': a.id, 'date': a.date.isoformat(), 'total_messages': a.total_messages,
                     'unique_users': a.unique_users, 'avg_response_time': a.avg_response_time,
                     'most_active_platform': a.most_active_platform} for a in analytics])

# Settings routes
@main.route('/settings/<int:user_id>', methods=['GET'])
def get_settings(user_id):
    settings = Settings.query.filter_by(user_id=user_id).first()
    if not settings:
        abort(404, description="Settings not found")
    return jsonify({'user_id': settings.user_id, 'default_view': settings.default_view, 'theme': settings.theme,
                    'notifications': settings.notifications, 'language': settings.language})

@main.route('/settings/<int:user_id>', methods=['PUT'])
def update_settings(user_id):
    settings = Settings.query.filter_by(user_id=user_id).first()
    if not settings:
        abort(404, description="Settings not found")
    data = request.get_json()
    if not data:
        abort(400, description="Missing data")
    settings.default_view = data.get('default_view', settings.default_view)
    settings.theme = data.get('theme', settings.theme)
    settings.notifications = data.get('notifications', settings.notifications)
    settings.language = data.get('language', settings.language)
    db.session.commit()
    return jsonify({'message': 'Settings updated'})

# New route to trigger data fetching from open source API
@main.route('/fetch-data/<string:platform_name>/<int:user_id>', methods=['POST'])
def fetch_data(platform_name, user_id):
    success, message = fetch_data_from_open_source_api(platform_name, user_id)
    if success:
        return jsonify({'message': message})
    else:
        abort(500, description=message)

    #route to chatbot


@main.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')

    
    response = f"You said: {user_input}"

    return jsonify({'response': response})

