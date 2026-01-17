from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Literal
from datetime import datetime
import re

# User Models
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: str

class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    created_at: datetime
    notification_preferences: dict = {
        "email": True,
        "sms": False,
        "whatsapp": False,
        "reminder_days_before": 3
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Existing Models (enhanced)
class MemberCreate(BaseModel):
    member_id: Optional[str] = None  # Auto-generated if not provided
    name: str
    phone: str
    email: Optional[EmailStr] = None
    monthly_amount: Optional[float] = 500  # Default ₹500
    due_day: Optional[int] = 5  # Default 5th of month

class Member(BaseModel):
    member_id: str
    name: str
    phone: str
    email: Optional[str] = None
    monthly_amount: float
    due_day: int
    created_at: datetime

class PaymentRecord(BaseModel):
    member_id: str
    amount: float
    due_date: str
    paid_date: Optional[str] = None

class PaymentSubmit(BaseModel):
    member_id: str
    contribution_id: str
    paid_date: str

class NotificationPreferences(BaseModel):
    email: bool = True
    sms: bool = False
    whatsapp: bool = False
    reminder_days_before: int = 3

class PredictionResult(BaseModel):
    member_id: str
    member_name: str
    risk_score: float
    likely_delay_days: int
    confidence: float
    factors: list
    recommendation: str

# Ticket System Models
class TicketCreate(BaseModel):
    request_type: Literal["monthly_amount", "due_day"]
    reason: str
    new_value: float  # Can be int or float depending on type
    
class Ticket(BaseModel):
    ticket_id: str
    member_id: str
    employee_id: str
    request_type: Literal["monthly_amount", "due_day"]
    reason: str
    current_value: float
    new_value: float
    status: Literal["pending", "approved", "rejected"] = "pending"
    created_at: datetime
    updated_at: Optional[datetime] = None
    admin_response: Optional[str] = None

# Employee ID Response
class EmployeeIDResponse(BaseModel):
    employee_id: str
    
# Phone validation
class PhoneValidatedModel(BaseModel):
    phone: str
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        # Remove spaces, dashes, and + sign
        cleaned = re.sub(r'[\s\-+]', '', v)
        # Check if it's 10 digits
        if not re.match(r'^\d{10}$', cleaned):
            raise ValueError('Phone number must be exactly 10 digits')
        return v

# Failed Payment Stats
class FailedPaymentStats(BaseModel):
    total_failed: int
    total_amount: float
    members_affected: int
    recent_failures: list

