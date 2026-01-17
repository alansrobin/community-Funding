"""
Test script for automated reminder scheduler endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Health check
print("=" * 60)
print("TEST 1: Health Check")
print("=" * 60)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# Get admin token first (you'll need to login)
print("=" * 60)
print("TEST 2: Admin Login")
print("=" * 60)
try:
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"phone": "9876543210", "password": "admin123"}
    )
    print(f"Status Code: {login_response.status_code}")
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        print(f"Token obtained: {token[:20]}...")
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print(f"Login failed: {login_response.text}")
        headers = {}
except Exception as e:
    print(f"Error: {e}")
    headers = {}

print("\n")

# Test 3: Check scheduler status
print("=" * 60)
print("TEST 3: Scheduler Status")
print("=" * 60)
try:
    response = requests.get(f"{BASE_URL}/admin/reminders/schedule", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# Test 4: Manually trigger reminder check
print("=" * 60)
print("TEST 4: Manual Trigger Reminder Check")
print("=" * 60)
try:
    response = requests.post(f"{BASE_URL}/admin/reminders/trigger", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# Test 5: Get reminder history
print("=" * 60)
print("TEST 5: Reminder History")
print("=" * 60)
try:
    response = requests.get(f"{BASE_URL}/admin/reminders/history?limit=10", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing complete!")
print("=" * 60)
