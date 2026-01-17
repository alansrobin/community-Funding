"""
Test MongoDB Atlas connection
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Get MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")

print("Testing MongoDB Atlas connection...")
print(f"MongoDB URI: {MONGO_URI[:50]}...")  # Print first 50 chars for security

try:
    # Create client
    client = MongoClient(MONGO_URI)
    
    # Test the connection
    client.admin.command('ping')
    print("✓ Successfully connected to MongoDB Atlas!")
    
    # List databases
    dbs = client.list_database_names()
    print(f"\nAvailable databases: {dbs}")
    
    # Get database name
    DATABASE_NAME = os.getenv("DATABASE_NAME", "contribution_tracking_db")
    db = client[DATABASE_NAME]
    
    # List collections in the database
    collections = db.list_collection_names()
    print(f"\nCollections in '{DATABASE_NAME}': {collections if collections else '(empty)'}")
    
    # Close connection
    client.close()
    print("\n✓ Connection test completed successfully!")
    
except Exception as e:
    print(f"\n✗ Error connecting to MongoDB: {str(e)}")
    print("\nPlease check:")
    print("1. Your MongoDB URI is correct")
    print("2. Network access is configured in MongoDB Atlas")
    print("3. Database user credentials are correct")
