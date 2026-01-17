"""
Check current database structure
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DATABASE_NAME')]

print("="*60)
print("CURRENT DATABASE STRUCTURE")
print("="*60)
print(f"\nDatabase: {db.name}")
print(f"Collections: {db.list_collection_names()}")

print("\n📊 MEMBERS COLLECTION:")
print("-"*60)
for member in db.members.find():
    print(f"  {member['member_id']:10} | {member['name']:20} | Role: {member['role']:6} | {member['email']}")

print("\n📊 CONTRIBUTIONS:")
print(f"  Total: {db.contributions.count_documents({})}")

client.close()
