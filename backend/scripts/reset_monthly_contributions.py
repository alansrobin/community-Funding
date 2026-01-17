from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "contribution_tracking_db")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Get current month
current_month = datetime.now().strftime("%Y-%m")
due_date = datetime.now().replace(day=5).strftime("%Y-%m-%d")

print(f"Deleting contributions for month: {current_month}")
print(f"Due date: {due_date}")

# Delete contributions for current month
result = db.contributions.delete_many({
    "due_date": due_date
})

print(f"\n✅ Deleted {result.deleted_count} contributions")
print(f"You can now click 'Generate Monthly Contributions' again!")
