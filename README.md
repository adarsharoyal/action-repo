<<<<<<< HEAD
# GitHub Webhook Receiver

A Flask-based webhook receiver that captures GitHub events (Push, Pull Request, Merge) and displays them in a real-time UI with MongoDB storage.

## Features

- Receives GitHub webhook events for Push, Pull Request, and Merge actions
- Stores event data in MongoDB
- Real-time UI that polls events every 15 seconds
- Clean and minimal design
- RESTful API endpoint to fetch events

## Prerequisites

- Python 3.8+
- MongoDB (local or cloud instance)
- GitHub repository (action-repo)
- Public endpoint for webhook receiver (use ngrok for local testing)

## Installation

### 1. Clone the Repository

```bash
git clone <your-webhook-repo-url>
cd webhook-repo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` file with your MongoDB configuration:

```
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=github_webhook_db
COLLECTION_NAME=events
FLASK_ENV=development
```

### 4. Install and Start MongoDB

**For Windows:**
```bash
# Download MongoDB from https://www.mongodb.com/try/download/community
# Install and start the MongoDB service
```

**For Mac (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**For Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Setting Up GitHub Webhook

### 1. Expose Local Server (for testing)

Use ngrok to expose your local server:

```bash
# Download ngrok from https://ngrok.com/download
ngrok http 5000
```

Copy the HTTPS forwarding URL (e.g., `https://abc123.ngrok.io`)

### 2. Configure Webhook in GitHub

1. Go to your GitHub repository (action-repo)
2. Navigate to **Settings** > **Webhooks** > **Add webhook**
3. Configure:
   - **Payload URL**: `https://your-ngrok-url.ngrok.io/webhook`
   - **Content type**: `application/json`
   - **Which events**: Select individual events:
     - ✅ Pushes
     - ✅ Pull requests
   - **Active**: ✅ Checked
4. Click **Add webhook**

## MongoDB Schema

The application stores events with the following schema:

```json
{
  "_id": "ObjectId",
  "request_id": "string (commit hash or PR ID)",
  "author": "string (GitHub username)",
  "action": "string (PUSH, PULL_REQUEST, MERGE)",
  "from_branch": "string",
  "to_branch": "string",
  "timestamp": "string (ISO 8601 datetime)"
}
```

## API Endpoints

### 1. Webhook Receiver
- **URL**: `/webhook`
- **Method**: POST
- **Description**: Receives GitHub webhook events
- **Headers Required**: `X-GitHub-Event`

### 2. Get Events
- **URL**: `/api/events`
- **Method**: GET
- **Description**: Fetches latest 20 events from MongoDB
- **Response**: JSON array of events

### 3. Health Check
- **URL**: `/health`
- **Method**: GET
- **Description**: Check if the server is running
- **Response**: `{"status": "healthy"}`

### 4. UI
- **URL**: `/`
- **Method**: GET
- **Description**: Renders the event monitoring UI

## Event Formats

### Push Event
```
{author} pushed to {to_branch} on {timestamp}
Example: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
```

### Pull Request Event
```
{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
Example: "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC
```

### Merge Event
```
{author} merged branch {from_branch} to {to_branch} on {timestamp}
Example: "Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC
```

## Testing

### Test Push Event

1. Make a commit to your action-repo:
```bash
git add .
git commit -m "Test commit"
git push origin main
```

2. Check the UI at `http://localhost:5000` - you should see the push event

### Test Pull Request Event

1. Create a new branch:
```bash
git checkout -b feature-branch
git push origin feature-branch
```

2. Create a pull request on GitHub from `feature-branch` to `main`
3. Check the UI - you should see the pull request event

### Test Merge Event

1. Merge the pull request on GitHub
2. Check the UI - you should see the merge event

## Project Structure

```
webhook-repo/
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # UI template
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Environment variables (create this)
└── README.md             # This file
```

## Deployment

### Deploy to Heroku

1. Create a Heroku app:
```bash
heroku create your-app-name
```

2. Add MongoDB addon:
```bash
heroku addons:create mongolab:sandbox
```

3. Set environment variables:
```bash
heroku config:set MONGO_URI=<your-mongodb-uri>
```

4. Deploy:
```bash
git push heroku main
```

### Deploy to Railway/Render

Follow similar steps as Heroku, ensuring MongoDB connection string is configured in environment variables.

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `sudo systemctl status mongodb`
- Check connection string in `.env` file
- Verify firewall settings allow MongoDB connection

### Webhook Not Receiving Events
- Verify ngrok is running and URL is correct
- Check GitHub webhook delivery status in repository settings
- Review application logs for errors

### UI Not Updating
- Check browser console for JavaScript errors
- Verify API endpoint `/api/events` returns data
- Check network tab in browser dev tools

## License

MIT

## Author

Built as part of Developer Assessment Task
=======
# action-repo
>>>>>>> 24d2cd961476e42668a71cee76fee1b2c5cb3016
