from pymongo import MongoClient
from datetime import datetime, timedelta
from app.auth import get_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use MongoDB connection from .env file
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "contribution_tracking_db")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Clear existing data
db.admins.delete_many({})
db.members.delete_many({})
db.contributions.delete_many({})
db.notifications.delete_many({})
db.predictions.delete_many({})

# Admin data (separate collection)
admin_data = [
    {
        "member_id": "ADMIN001",
        "name": "Administrator",
        "phone": "+91-9999999999",
        "email": "admin@contribution.com",
        "password_hash": get_password_hash("admin123"),
        "role": "admin",
        "monthly_amount": 0,
        "due_day": 1,
        "notification_preferences": {
            "email": True,
            "sms": False,
            "whatsapp": False,
            "reminder_days_before": 3
        },
        "created_at": datetime.now()
    }
]

# Member data (regular members only)
members_data = [
    {
        "member_id": "M001",
        "name": "Arun Kumar",
        "phone": "+91-9876543210",
        "email": "arun.kumar@email.com",
        "password_hash": get_password_hash("password123"),
        "role": "member",
        "monthly_amount": 500,
        "due_day": 5,
        "notification_preferences": {
            "email": True,
            "sms": True,
            "whatsapp": False,
            "reminder_days_before": 3
        },
        "created_at": datetime.now()
    },
    {
        "member_id": "M002",
        "name": "Beena Joseph",
        "phone": "+91-9876543211",
        "email": "beena.joseph@email.com",
        "password_hash": get_password_hash("password123"),
        "role": "member",
        "monthly_amount": 500,
        "due_day": 5,
        "notification_preferences": {
            "email": True,
            "sms": False,
            "whatsapp": True,
            "reminder_days_before": 5
        },
        "created_at": datetime.now()
    },
    {
        "member_id": "M003",
        "name": "Charan Singh",
        "phone": "+91-9876543212",
        "email": "charan.singh@email.com",
        "password_hash": get_password_hash("password123"),
        "role": "member",
        "monthly_amount": 500,
        "due_day": 5,
        "notification_preferences": {
            "email": True,
            "sms": True,
            "whatsapp": True,
            "reminder_days_before": 2
        },
        "created_at": datetime.now()
    },
    {
        "member_id": "M004",
        "name": "Divya Nair",
        "phone": "+91-9876543213",
        "email": "divya.nair@email.com",
        "password_hash": get_password_hash("password123"),
        "role": "member",
        "monthly_amount": 500,
        "due_day": 5,
        "notification_preferences": {
            "email": True,
            "sms": False,
            "whatsapp": False,
            "reminder_days_before": 3
        },
        "created_at": datetime.now()
    },
    {
        "member_id": "M005",
        "name": "Eswar Reddy",
        "phone": "+91-9876543214",
        "email": "eswar.reddy@email.com",
        "password_hash": get_password_hash("password123"),
        "role": "member",
        "monthly_amount": 500,
        "due_day": 5,
        "notification_preferences": {
            "email": False,
            "sms": True,
            "whatsapp": False,
            "reminder_days_before": 3
        },
        "created_at": datetime.now()
    }
]

# Insert into separate collections
db.admins.insert_many(admin_data)
db.members.insert_many(members_data)

# Generate contribution records
contributions_data = []

def create_contribution(member_id, month_offset, amount, paid_offset=None):
    base_date = datetime.now() - timedelta(days=30 * month_offset)
    due_date = base_date.replace(day=5).strftime("%Y-%m-%d")
    
    contribution = {
        "member_id": member_id,
        "due_date": due_date,
        "amount": amount,
        "paid_date": None
    }
    
    if paid_offset is not None:
        paid_date = datetime.strptime(due_date, "%Y-%m-%d") + timedelta(days=paid_offset)
        contribution["paid_date"] = paid_date.strftime("%Y-%m-%d")
    
    return contribution

# M001 - Regular
for i in range(6, 0, -1):
    contributions_data.append(create_contribution("M001", i, 500, paid_offset=2))

# M002 - Occasional delay
contributions_data.append(create_contribution("M002", 6, 500, paid_offset=1))
contributions_data.append(create_contribution("M002", 5, 500, paid_offset=10))
contributions_data.append(create_contribution("M002", 4, 500, paid_offset=3))
contributions_data.append(create_contribution("M002", 3, 500, paid_offset=15))
contributions_data.append(create_contribution("M002", 2, 500, paid_offset=5))
contributions_data.append(create_contribution("M002", 1, 500, paid_offset=None))

# M003 - High-risk
contributions_data.append(create_contribution("M003", 6, 500, paid_offset=None))
contributions_data.append(create_contribution("M003", 5, 500, paid_offset=None))
contributions_data.append(create_contribution("M003", 4, 500, paid_offset=45))
contributions_data.append(create_contribution("M003", 3, 500, paid_offset=None))
contributions_data.append(create_contribution("M003", 2, 500, paid_offset=None))
contributions_data.append(create_contribution("M003", 1, 500, paid_offset=None))

# M004 - Regular
for i in range(6, 0, -1):
    contributions_data.append(create_contribution("M004", i, 500, paid_offset=5))

# M005 - Occasional delay
contributions_data.append(create_contribution("M005", 6, 500, paid_offset=3))
contributions_data.append(create_contribution("M005", 5, 500, paid_offset=8))
contributions_data.append(create_contribution("M005", 4, 500, paid_offset=1))
contributions_data.append(create_contribution("M005", 3, 500, paid_offset=12))
contributions_data.append(create_contribution("M005", 2, 500, paid_offset=None))
contributions_data.append(create_contribution("M005", 1, 500, paid_offset=None))

db.contributions.insert_many(contributions_data)

# Print summary
print("=" * 60)
print("ENHANCED DATABASE INITIALIZED")
print("=" * 60)
print(f"\nTotal Members: {len(members_data)}")
print(f"Total Contributions: {len(contributions_data)}")
print("\n🔐 LOGIN CREDENTIALS:")
print("-" * 60)
print("Admin Account:")
print("  Email: admin@contribution.com")
print("  Password: admin123")
print("\nMember Accounts (all use password: password123):")
for member in members_data:
    if member["role"] == "member":
        print(f"  {member['name']}: {member['email']}")
print("\n" + "=" * 60)
print("✅ Database ready with authentication enabled!")
print("=" * 60)
