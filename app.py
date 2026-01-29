from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

app = Flask(__name__)
CORS(app)

# -------------------------
# MongoDB Configuration
# -------------------------
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise Exception("❌ MONGO_URI not found. Check your .env file.")

DATABASE_NAME = os.getenv('DATABASE_NAME', 'github_webhook_db')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'events')

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# -------------------------
# Utility function
# -------------------------
def format_timestamp(timestamp_str):
    """Convert ISO timestamp to readable format"""
    try:
        dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime('%d%s %B %Y - %I:%M %p UTC') % (
            dt.day,
            'th' if 11 <= dt.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(dt.day % 10, 'th')
        )
    except:
        return timestamp_str

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    """Render the UI"""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/events', methods=['GET'])
def get_events():
    """API endpoint to fetch latest events"""
    try:
        events = list(collection.find().sort('timestamp', -1).limit(20))
        for event in events:
            event['_id'] = str(event['_id'])
        return jsonify(events), 200
    except Exception as e:
        print(f"❌ Error fetching events: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint to receive GitHub webhooks"""
    try:
        if not request.is_json:
            print("❌ Received non-JSON payload")
            return jsonify({'error': 'Payload must be JSON'}), 400

        payload = request.get_json()
        headers = request.headers

        # Debug logs
        print("Incoming webhook payload:", payload)
        event_type = headers.get('X-GitHub-Event', '').lower()
        print("GitHub Event Type:", event_type)

        # Route events
        if event_type == 'push':
            handle_push_event(payload)
        elif event_type == 'pull_request':
            handle_pull_request_event(payload)
        else:
            print("⚠️ Unsupported event type:", event_type)
            return jsonify({'message': 'Event type not supported'}), 200

        return jsonify({'message': 'Webhook received successfully'}), 200

    except Exception as e:
        print(f"❌ Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

# -------------------------
# Event Handlers
# -------------------------
def handle_push_event(payload):
    """Handle push events"""
    if not payload:
        print("❌ Empty push payload received")
        return

    ref = payload.get('ref', '')
    to_branch = ref.split('/')[-1] if '/' in ref else ref
    head_commit = payload.get('head_commit', {})
    timestamp = head_commit.get('timestamp', datetime.utcnow().isoformat() + 'Z')

    event_data = {
        'request_id': payload.get('after', ''),
        'author': payload.get('pusher', {}).get('name', 'Unknown'),
        'action': 'PUSH',
        'from_branch': '',
        'to_branch': to_branch,
        'timestamp': timestamp
    }

    collection.insert_one(event_data)
    print(f"✅ Push event saved: {event_data}")

def handle_pull_request_event(payload):
    """Handle pull request events (including merged PRs)"""
    pr_data = payload.get('pull_request', {})
    if not pr_data:
        print("❌ Empty pull_request payload received")
        return

    action = payload.get('action', '')
    is_merged = action == 'closed' and pr_data.get('merged', False)
    event_action = 'MERGE' if is_merged else 'PULL_REQUEST'

    # Use merged_at timestamp for MERGE, updated_at otherwise
    timestamp = pr_data.get('merged_at') if is_merged else pr_data.get('updated_at')
    if not timestamp:
        timestamp = datetime.utcnow().isoformat() + 'Z'

    event_data = {
        'request_id': str(pr_data.get('id', '')),
        'author': pr_data.get('user', {}).get('login', 'Unknown'),
        'action': event_action,
        'from_branch': pr_data.get('head', {}).get('ref', ''),
        'to_branch': pr_data.get('base', {}).get('ref', ''),
        'timestamp': timestamp
    }

    collection.insert_one(event_data)
    print(f"✅ Pull request event saved: {event_data}")

# -------------------------
# Run Flask App
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
