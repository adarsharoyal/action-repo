# Complete Setup Guide for GitHub Webhook Project

This guide will walk you through setting up both repositories (action-repo and webhook-repo) for the GitHub webhook project.

## Part 1: Setting Up webhook-repo (This Repository)

### Step 1: Clone and Install

```bash
# Clone this repository
git clone <webhook-repo-url>
cd webhook-repo

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install and Configure MongoDB

#### Option A: Local MongoDB Installation

**Windows:**
1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Run the installer
3. MongoDB will start automatically as a Windows service

**Mac (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

#### Option B: MongoDB Atlas (Cloud - Free Tier)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for a free account
3. Create a new cluster (M0 free tier)
4. Create a database user
5. Whitelist your IP address (or use 0.0.0.0/0 for testing)
6. Get your connection string (replace <password> with your database user password)

### Step 3: Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env file with your MongoDB connection string
# For local MongoDB:
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=github_webhook_db
COLLECTION_NAME=events

# For MongoDB Atlas:
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=github_webhook_db
COLLECTION_NAME=events
```

### Step 4: Test Local Server

```bash
# Start the Flask application
python app.py

# In a new terminal, run the test script
python test_webhook.py

# Open browser and visit: http://localhost:5000
# You should see the test events displayed
```

### Step 5: Expose Local Server with ngrok

```bash
# Download ngrok from https://ngrok.com/download
# Extract and run:
ngrok http 5000

# Copy the HTTPS forwarding URL (e.g., https://abc123.ngrok.io)
# You'll use this in the GitHub webhook configuration
```

## Part 2: Setting Up action-repo

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Name it `action-repo`
3. Choose Public or Private
4. Initialize with a README
5. Click "Create repository"

### Step 2: Clone the Repository Locally

```bash
git clone https://github.com/yourusername/action-repo.git
cd action-repo
```

### Step 3: Configure GitHub Webhook

1. Go to your `action-repo` on GitHub
2. Click **Settings** (top menu)
3. Click **Webhooks** (left sidebar)
4. Click **Add webhook** button

Configure the webhook:
- **Payload URL**: `https://your-ngrok-url.ngrok.io/webhook`
  - Replace `your-ngrok-url` with the ngrok URL from Step 5 above
  - Example: `https://abc123.ngrok.io/webhook`
- **Content type**: Select `application/json`
- **Secret**: Leave blank (or add for security)
- **Which events would you like to trigger this webhook?**
  - Select "Let me select individual events"
  - Check: ✅ Pushes
  - Check: ✅ Pull requests
  - Uncheck everything else
- **Active**: ✅ Ensure this is checked

5. Click **Add webhook**

### Step 4: Verify Webhook Configuration

1. GitHub will send a ping event to test the webhook
2. You should see a green checkmark ✓ if successful
3. Click on the webhook to view delivery details
4. Check "Recent Deliveries" tab to see the ping event

## Part 3: Testing the Complete Setup

### Test 1: Push Event

```bash
# In your action-repo directory
echo "# Test Push" >> test.txt
git add test.txt
git commit -m "Test push event"
git push origin main

# Check http://localhost:5000 in your browser
# You should see the push event displayed
```

### Test 2: Pull Request Event

```bash
# Create a new branch
git checkout -b feature-test
echo "# Feature Test" >> feature.txt
git add feature.txt
git commit -m "Add feature"
git push origin feature-test

# Go to GitHub and create a Pull Request
# 1. Navigate to your action-repo on GitHub
# 2. Click "Pull requests" tab
# 3. Click "New pull request"
# 4. Select base: main, compare: feature-test
# 5. Click "Create pull request"
# 6. Add a title and click "Create pull request"

# Check http://localhost:5000
# You should see the pull request event
```

### Test 3: Merge Event

```bash
# On GitHub, merge the pull request you just created
# 1. Open the pull request
# 2. Click "Merge pull request"
# 3. Click "Confirm merge"

# Check http://localhost:5000
# You should see the merge event
```

## Part 4: Verification Checklist

- [ ] MongoDB is running and accessible
- [ ] Flask app starts without errors (`python app.py`)
- [ ] Test script creates events successfully (`python test_webhook.py`)
- [ ] UI loads at http://localhost:5000
- [ ] UI displays test events
- [ ] ngrok is running and providing HTTPS URL
- [ ] GitHub webhook is configured with ngrok URL
- [ ] GitHub webhook shows green checkmark (successful ping)
- [ ] Push events are captured and displayed
- [ ] Pull request events are captured and displayed
- [ ] Merge events are captured and displayed

## Part 5: Deployment to Production (Optional)

### Deploy webhook-repo to Heroku

```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-webhook-app-name

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# The MONGO_URI will be set automatically as MONGODB_URI
# Deploy the app
git push heroku main

# Open the app
heroku open

# Update GitHub webhook URL to use Heroku URL
# https://your-webhook-app-name.herokuapp.com/webhook
```

### Alternative: Deploy to Render.com

1. Go to https://render.com
2. Sign up/Login
3. Click "New +" and select "Web Service"
4. Connect your webhook-repo GitHub repository
5. Configure:
   - Name: your-webhook-app
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
6. Add Environment Variables:
   - MONGO_URI: (your MongoDB Atlas connection string)
   - DATABASE_NAME: github_webhook_db
   - COLLECTION_NAME: events
7. Click "Create Web Service"
8. Update GitHub webhook URL to use Render URL

## Troubleshooting

### Issue: MongoDB connection failed

**Solution:**
- Check if MongoDB service is running
- Verify MONGO_URI in .env file
- For MongoDB Atlas, check IP whitelist and credentials

### Issue: GitHub webhook not receiving events

**Solution:**
- Verify ngrok is still running (it times out after 2 hours on free plan)
- Check webhook URL in GitHub settings
- Review webhook delivery logs in GitHub
- Check Flask app logs for errors

### Issue: UI not updating

**Solution:**
- Check browser console for JavaScript errors
- Verify `/api/events` endpoint returns data
- Check MongoDB has events stored
- Clear browser cache

### Issue: Events not displaying in correct format

**Solution:**
- Verify event data structure in MongoDB
- Check timestamp format (should be ISO 8601)
- Review browser console logs

## Additional Resources

- [GitHub Webhooks Documentation](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [ngrok Documentation](https://ngrok.com/docs)

## Support

If you encounter any issues not covered in this guide, please:
1. Check the error logs in the terminal
2. Review GitHub webhook delivery details
3. Verify all configuration values are correct
4. Test with the provided test script first

Good luck with your implementation!
