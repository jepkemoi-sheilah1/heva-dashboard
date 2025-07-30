import requests
from app.models import db, Message, Platform, User
from datetime import datetime

def fetch_data_from_open_source_api(platform_name, user_id):
    """
    Example function to fetch data from an open source API for a given platform
    and store the data in the database as Messages.
    """
    # Example API endpoint for demonstration (replace with actual open source API)
    api_url = f"https://api.example.com/{platform_name}/data"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Find the platform in the database
        platform = Platform.query.filter_by(name=platform_name).first()
        if not platform:
            # If platform does not exist, create it
            platform = Platform()
            platform.name = platform_name
            platform.icon_url = ''
            platform.is_active = True
            db.session.add(platform)
            db.session.commit()

        # Process and store data as Messages
        for item in data.get('messages', []):
            message = Message()
            message.content = item.get('content', '')
            message.direction = 'incoming'
            message.user_id = user_id
            message.platform_id = platform.id
            message.timestamp = datetime.utcnow()
            db.session.add(message)

        db.session.commit()
        return True, f"Data fetched and stored for platform {platform_name}"

    except requests.RequestException as e:
        return False, str(e)
