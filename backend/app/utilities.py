"""
Utility functions for the Contribution Tracking API.
Contains helper functions used across multiple modules.
"""
from datetime import datetime
from typing import Optional
import random
import re

from .db import members_collection


def generate_employee_id() -> str:
    """Generate unique employee ID with format EMP-YYYYMMDD-XXXX"""
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    employee_id = f"EMP-{date_part}-{random_part}"
    
    # Ensure uniqueness
    while members_collection.find_one({"employee_id": employee_id}):
        random_part = random.randint(1000, 9999)
        employee_id = f"EMP-{date_part}-{random_part}"
    
    return employee_id


def generate_member_id() -> str:
    """Generate unique member ID with format M001, M002, etc."""
    # Find the highest member number
    all_members = list(members_collection.find({}, {"member_id": 1}))
    
    if not all_members:
        return "M001"
    
    # Extract numbers from member IDs like M001, M002, etc.
    max_num = 0
    for member in all_members:
        member_id = member.get("member_id", "")
        if member_id.startswith("M") and len(member_id) > 1:
            try:
                num = int(member_id[1:])
                max_num = max(max_num, num)
            except ValueError:
                continue
    
    # Generate next member ID
    next_num = max_num + 1
    return f"M{next_num:03d}"  # Format: M001, M002, etc.


def validate_phone(phone: str) -> bool:
    """Validate phone number (10 digits)"""
    cleaned = re.sub(r'[\s\-+]', '', phone)
    return bool(re.match(r'^\d{10}$', cleaned))


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def calculate_delay_days(due_date_str: str, paid_date_str: Optional[str] = None) -> int:
    """Calculate delay days from due date"""
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    compare_date = datetime.strptime(paid_date_str, "%Y-%m-%d") if paid_date_str else datetime.now()
    delay = (compare_date - due_date).days
    return max(0, delay)


def classify_member(missed_payments: int, avg_delay_days: float) -> str:
    """Classify member based on payment history
    
    Priority: Members with no current unpaid dues are always classified as Regular,
    regardless of past payment delays.
    """
    # If all dues are paid (no missed payments), member is Regular
    if missed_payments == 0:
        return "Regular"
    # Otherwise, classify based on delay patterns
    elif missed_payments <= 2 and avg_delay_days <= 15:
        return "Occasional Delay"
    else:
        return "High-risk Delay"


def calculate_payment_status(contribution):
    """
    Calculate detailed payment status with 5-day grace period.
    
    Returns: "regular", "delayed", "pending", or "overdue"
    """
    if contribution.get("paid_date") is None:
        # Unpaid contribution - check if overdue
        due_date = datetime.strptime(contribution["due_date"], "%Y-%m-%d")
        today = datetime.now()
        days_since_due = (today - due_date).days
        
        if days_since_due > 5:
            return "overdue"  # Past grace period, still unpaid (urgent)
        elif days_since_due >= 0:
            return "pending"  # Within grace period
        else:
            return "future"   # Not yet due
    
    # Payment made - check if within 5-day grace period
    due_date = datetime.strptime(contribution["due_date"], "%Y-%m-%d")
    paid_date = datetime.strptime(contribution["paid_date"], "%Y-%m-%d")
    delay_days = (paid_date - due_date).days
    
    if delay_days <= 5:
        return "regular"  # Paid within 5-day grace period
    else:
        return "delayed"  # Paid but beyond grace period


def calculate_member_status(contributions):
    """
    Calculate member's overall status based on payment history.
    
    Looks at last 6 contributions and classifies as:
    - regular: All payments within grace period
    - occasional_delay: Some delays (< 33%)
    - high_risk: Frequent delays (≥ 33%)
    """
    if not contributions:
        return "new"  # New member with no history
    
    # Look at last 6 months (or all if less than 6)
    recent = contributions[-6:] if len(contributions) >= 6 else contributions
    
    # Count delayed payments (beyond 5-day grace period)
    delayed_count = 0
    for contrib in recent:
        status = calculate_payment_status(contrib)
        if status in ["delayed", "overdue"]:
            delayed_count += 1
    
    # Calculate delay percentage
    delay_percentage = delayed_count / len(recent) if recent else 0
    
    # Classify member status
    if delay_percentage == 0:
        return "regular"
    elif delay_percentage < 0.33:  # Less than 33% delayed
        return "occasional_delay"
    else:  # 33% or more delayed
        return "high_risk"


def get_member_status_info(status):
    """
    Get display information for member status.
    
    Returns dict with color, label, and description.
    """
    status_map = {
        "regular": {
            "color": "green",
            "label": "Regular",
            "description": "Consistent on-time payments within grace period"
        },
        "occasional_delay": {
            "color": "yellow",
            "label": "Occasional Delay",
            "description": "Some delayed payments, needs attention"
        },
        "high_risk": {
            "color": "red",
            "label": "High Risk",
            "description": "Frequent delays, requires proactive outreach"
        },
        "new": {
            "color": "blue",
            "label": "New Member",
            "description": "Insufficient payment history"
        }
    }
    
    return status_map.get(status, status_map["new"])


def get_payment_status(contribution: dict) -> str:
    """Get payment status for a contribution"""
    if contribution.get("paid_date"):
        return "Paid"
    else:
        delay_days = calculate_delay_days(contribution["due_date"], None)
        if delay_days > 30:
            return "Delayed"
        elif delay_days > 0:
            return "Unpaid"
        else:
            return "Pending"