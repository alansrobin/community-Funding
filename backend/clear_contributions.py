"""
Quick script to clear existing contributions for testing
This allows you to test the email automation again
"""
from app.db import contributions_collection
from datetime import datetime

# Get current month
now = datetime.now()
current_month = f"{now.year}-{now.month:02d}"

# Delete all contributions for current month
result = contributions_collection.delete_many({"month": current_month})

print(f"✅ Cleared {result.deleted_count} contributions for {current_month}")
