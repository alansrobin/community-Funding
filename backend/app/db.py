"""
Database configuration and connection module.
Handles MongoDB connection using environment variables.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "contribution_tracking_db")

# MongoDB Client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Collections
admins_collection = db.admins  # Admin users only
members_collection = db.members  # Regular members only
contributions_collection = db.contributions
notifications_collection = db.notifications
predictions_collection = db.predictions
tickets_collection = db.tickets


def get_database():
    """Get database instance"""
    return db


def get_collection(collection_name: str):
    """Get a specific collection by name"""
    return db[collection_name]


def close_connection():
    """Close MongoDB connection"""
    client.close()
