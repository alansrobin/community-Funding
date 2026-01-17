"""
MongoDB User Setup Script
Creates a demo user with test password for authentication.
"""
from pymongo import MongoClient

# Connect to MongoDB without authentication (admin access needed)
client = MongoClient("mongodb://localhost:27017/")

# Select the database
db = client.contribution_tracking_db

try:
    # Create user with username: demo, password: test
    db.command(
        "createUser",
        "demo",
        pwd="test",
        roles=[
            {
                "role": "readWrite",
                "db": "contribution_tracking_db"
            }
        ]
    )
    print("✅ User 'demo' created successfully!")
    print("Username: demo")
    print("Password: test")
    print("Database: contribution_tracking_db")
    
except Exception as e:
    if "already exists" in str(e):
        print("ℹ️  User 'demo' already exists")
    else:
        print(f"❌ Error: {e}")
        print("\nNote: You may need to run MongoDB without authentication first")
        print("or connect as admin to create users.")

client.close()
