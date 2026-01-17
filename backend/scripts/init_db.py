from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["contribution_tracking_db"]

# Clear existing data
db.members.delete_many({})
db.contributions.delete_many({})

# Sample member data with varied payment patterns
members_data = [
    {
        "member_id": "M001",
        "name": "Arun Kumar",
        "phone": "+91-9876543210",
        "email": "arun.kumar@email.com",
        "monthly_amount": 1000,
        "due_day": 5,
        "created_at": datetime.now()
    },
    {
        "member_id": "M002",
        "name": "Beena Joseph",
        "phone": "+91-9876543211",
        "email": "beena.joseph@email.com",
        "monthly_amount": 1500,
        "due_day": 10,
        "created_at": datetime.now()
    },
    {
        "member_id": "M003",
        "name": "Charan Singh",
        "phone": "+91-9876543212",
        "email": "charan.singh@email.com",
        "monthly_amount": 1000,
        "due_day": 1,
        "created_at": datetime.now()
    },
    {
        "member_id": "M004",
        "name": "Divya Nair",
        "phone": "+91-9876543213",
        "email": "divya.nair@email.com",
        "monthly_amount": 2000,
        "due_day": 15,
        "created_at": datetime.now()
    },
    {
        "member_id": "M005",
        "name": "Eswar Reddy",
        "phone": "+91-9876543214",
        "email": None,
        "monthly_amount": 1000,
        "due_day": 5,
        "created_at": datetime.now()
    }
]

db.members.insert_many(members_data)

# Generate contribution records with varied payment patterns
contributions_data = []

# Helper function to create contribution
def create_contribution(member_id, month_offset, amount, paid_offset=None):
    """Create a contribution record"""
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

# M001 - Regular member (always pays on time)
for i in range(6, 0, -1):
    contributions_data.append(create_contribution("M001", i, 1000, paid_offset=2))

# M002 - Occasional delay (sometimes delays by 1-2 weeks)
contributions_data.append(create_contribution("M002", 6, 1500, paid_offset=1))
contributions_data.append(create_contribution("M002", 5, 1500, paid_offset=10))
contributions_data.append(create_contribution("M002", 4, 1500, paid_offset=3))
contributions_data.append(create_contribution("M002", 3, 1500, paid_offset=15))
contributions_data.append(create_contribution("M002", 2, 1500, paid_offset=5))
contributions_data.append(create_contribution("M002", 1, 1500, paid_offset=None))  # Current month unpaid

# M003 - High-risk (multiple missed payments, long delays)
contributions_data.append(create_contribution("M003", 6, 1000, paid_offset=None))  # Missed
contributions_data.append(create_contribution("M003", 5, 1000, paid_offset=None))  # Missed
contributions_data.append(create_contribution("M003", 4, 1000, paid_offset=45))  # Very late
contributions_data.append(create_contribution("M003", 3, 1000, paid_offset=None))  # Missed
contributions_data.append(create_contribution("M003", 2, 1000, paid_offset=None))  # Missed
contributions_data.append(create_contribution("M003", 1, 1000, paid_offset=None))  # Current month unpaid

# M004 - Regular member (consistent, slight delays)
for i in range(6, 0, -1):
    contributions_data.append(create_contribution("M004", i, 2000, paid_offset=5))

# M005 - Occasional delay
contributions_data.append(create_contribution("M005", 6, 1000, paid_offset=3))
contributions_data.append(create_contribution("M005", 5, 1000, paid_offset=8))
contributions_data.append(create_contribution("M005", 4, 1000, paid_offset=1))
contributions_data.append(create_contribution("M005", 3, 1000, paid_offset=12))
contributions_data.append(create_contribution("M005", 2, 1000, paid_offset=None))  # Missed
contributions_data.append(create_contribution("M005", 1, 1000, paid_offset=None))  # Current month unpaid

db.contributions.insert_many(contributions_data)

# Print summary
print("=" * 60)
print("DATABASE INITIALIZED SUCCESSFULLY")
print("=" * 60)
print(f"\nTotal Members: {len(members_data)}")
print(f"Total Contributions: {len(contributions_data)}")
print("\nMember Summary:")
print("-" * 60)
for member in members_data:
    print(f"  {member['member_id']}: {member['name']} - ₹{member['monthly_amount']}/month")
print("\nPayment Pattern Summary:")
print("-" * 60)
print("  M001 (Arun Kumar): Regular - Always on time")
print("  M002 (Beena Joseph): Occasional Delay - Sometimes late")
print("  M003 (Charan Singh): High-risk - Multiple missed payments")
print("  M004 (Divya Nair): Regular - Consistent, slight delays")
print("  M005 (Eswar Reddy): Occasional Delay - Some missed")
print("\n" + "=" * 60)
print("You can now start the backend server:")
print("  cd backend && uvicorn main:app --reload")
print("=" * 60)
