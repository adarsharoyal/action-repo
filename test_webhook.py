"""
Test script to simulate GitHub webhook events
Run this script to test the webhook endpoint locally
"""

import requests
import json
from datetime import datetime

WEBHOOK_URL = "http://localhost:5000/webhook"

# Test Push Event
def test_push_event():
    payload = {
        "ref": "refs/heads/main",
        "after": "abc123def456",
        "pusher": {
            "name": "Travis"
        },
        "head_commit": {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    }

    headers = {
        "X-GitHub-Event": "push",
        "Content-Type": "application/json"
    }

    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Push Event Response: {response.status_code} - {response.json()}")

# Test Pull Request Event
def test_pull_request_event():
    payload = {
        "action": "opened",
        "pull_request": {
            "id": 123456,
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            },
            "updated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "merged": False
        }
    }

    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json"
    }

    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Pull Request Event Response: {response.status_code} - {response.json()}")

# Test Merge Event (Closed PR with merged=true)
def test_merge_event():
    payload = {
        "action": "closed",
        "pull_request": {
            "id": 789012,
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "dev"
            },
            "base": {
                "ref": "master"
            },
            "updated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "merged": True
        }
    }

    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json"
    }

    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Merge Event Response: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    print("Testing GitHub Webhook Endpoints...")
    print("\n" + "="*50)

    print("\n1. Testing Push Event...")
    test_push_event()

    print("\n2. Testing Pull Request Event...")
    test_pull_request_event()

    print("\n3. Testing Merge Event...")
    test_merge_event()

    print("\n" + "="*50)
    print("\nAll tests completed! Check http://localhost:5000 to view the events.")
