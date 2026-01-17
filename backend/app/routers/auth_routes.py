"""
Authentication routes for the Contribution Tracking API.
Handles user registration, login, and profile management.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta

from ..db import admins_collection, members_collection
from ..models import UserCreate, UserLogin, Token
from ..auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_current_user
from ..utilities import validate_phone, generate_employee_id

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    """Register a new user"""
    # Check if user exists
    if members_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate phone
    if not validate_phone(user.phone):
        raise HTTPException(status_code=400, detail="Invalid phone number. Must be 10 digits.")
    
    # Auto-generate member_id (format: M001, M002, etc.)
    existing_members = list(members_collection.find({"member_id": {"$regex": "^M\\d+$"}}))
    if existing_members:
        # Extract numbers from member_ids and find max
        member_numbers = [int(m["member_id"][1:]) for m in existing_members if m["member_id"][1:].isdigit()]
        next_number = max(member_numbers) + 1 if member_numbers else 1
    else:
        next_number = 1
    member_id = f"M{next_number:03d}"
    
    # Generate employee ID
    employee_id = generate_employee_id()
    
    # Create user (monthly_amount and due_day will be set by admin later)
    user_dict = {
        "member_id": member_id,
        "employee_id": employee_id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "password_hash": get_password_hash(user.password),
        "role": "member",
        "monthly_amount": None,  # To be set by admin
        "due_day": None,  # To be set by admin
        "notification_preferences": {
            "email": True,
            "sms": False,
            "whatsapp": False,
            "reminder_days_before": 3
        },
        "created_at": datetime.now()
    }
    
    members_collection.insert_one(user_dict)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": "member"},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    """Login and get access token"""
    # Check admins collection first
    user = admins_collection.find_one({"email": user_login.email})
    
    # If not found, check members collection
    if not user:
        user = members_collection.find_one({"email": user_login.email})
    
    if not user or not verify_password(user_login.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user.get("role", "member")},
        expires_delta=access_token_expires
    )
    
    # Check if password change is required
    must_change_password = user.get("must_change_password", False)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "must_change_password": must_change_password
    }


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "member_id": current_user["member_id"],
        "email": current_user["email"],
        "name": current_user["name"],
        "phone": current_user["phone"],
        "role": current_user.get("role", "member"),
        "monthly_amount": current_user["monthly_amount"],
        "due_day": current_user["due_day"],
        "notification_preferences": current_user.get("notification_preferences", {})
    }
