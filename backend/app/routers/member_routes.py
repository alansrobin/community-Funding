"""
Member routes for the Contribution Tracking API.
Handles member dashboard, contributions, notifications, and preferences.
"""
from fastapi import APIRouter, Depends
from datetime import datetime

from ..db import members_collection, contributions_collection, notifications_collection
from ..models import NotificationPreferences
from ..dependencies import get_current_user
from ..utilities import calculate_delay_days, classify_member, get_payment_status

router = APIRouter()


@router.get("/dashboard")
async def member_dashboard(current_user: dict = Depends(get_current_user)):
    """Get member's personal dashboard"""
    member_id = current_user["member_id"]
    
    # Get contributions
    contributions = list(contributions_collection.find({"member_id": member_id}))
    
    # Calculate statistics
    total_contributions = len(contributions)
    paid_count = sum(1 for c in contributions if c.get("paid_date"))
    missed_count = total_contributions - paid_count
    
    # Calculate delays
    delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
              for c in contributions if c.get("paid_date")]
    avg_delay = sum(delays) / len(delays) if delays else 0
    
    # Get upcoming dues
    upcoming = []
    for c in contributions:
        if not c.get("paid_date"):
            due_date = datetime.strptime(c["due_date"], "%Y-%m-%d")
            days_until = (due_date - datetime.now()).days
            upcoming.append({
                "contribution_id": str(c["_id"]),
                "due_date": c["due_date"],
                "amount": c["amount"],
                "days_until": days_until,
                "status": "overdue" if days_until < 0 else "upcoming"
            })
    
    # Classification
    classification = classify_member(missed_count, avg_delay)
    
    return {
        "member_info": {
            "name": current_user["name"],
            "member_id": member_id,
            "monthly_amount": current_user["monthly_amount"]
        },
        "statistics": {
            "total_contributions": total_contributions,
            "paid_count": paid_count,
            "missed_count": missed_count,
            "avg_delay_days": round(avg_delay, 1),
            "classification": classification
        },
        "upcoming_dues": upcoming,
        "total_pending": sum(c["amount"] for c in contributions if not c.get("paid_date"))
    }


@router.get("/contributions")
async def get_member_contributions(current_user: dict = Depends(get_current_user)):
    """Get member's contribution history"""
    member_id = current_user["member_id"]
    contributions = list(contributions_collection.find({"member_id": member_id}))
    
    formatted = []
    for c in contributions:
        formatted.append({
            "id": str(c["_id"]),
            "due_date": c["due_date"],
            "paid_date": c.get("paid_date"),
            "amount": c["amount"],
            "status": get_payment_status(c),
            "delay_days": calculate_delay_days(c["due_date"], c.get("paid_date"))
        })
    
    return formatted


@router.get("/notifications")
async def get_member_notifications(current_user: dict = Depends(get_current_user)):
    """Get member's notification history"""
    member_id = current_user["member_id"]
    notifications = list(notifications_collection.find({"member_id": member_id}).sort("sent_at", -1).limit(20))
    
    return [{
        "id": str(n["_id"]),
        "type": n["notification_type"],
        "sent_at": n["sent_at"],
        "message": n["message"],
        "status": n.get("status", "sent")
    } for n in notifications]


@router.post("/preferences")
async def update_preferences(
    preferences: NotificationPreferences,
    current_user: dict = Depends(get_current_user)
):
    """Update notification preferences"""
    members_collection.update_one(
        {"member_id": current_user["member_id"]},
        {"$set": {"notification_preferences": preferences.dict()}}
    )
    return {"status": "success", "message": "Preferences updated"}


@router.get("/impact/stats")
async def get_community_impact(current_user: dict = Depends(get_current_user)):
    """Get community impact statistics (Simulated for MVP)"""
    
    # Calculate real total from DB
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
    result = list(contributions_collection.aggregate(pipeline))
    total_raised = result[0]["total"] if result else 0
    
    # Simulated Goal and Projects
    GOAL = 500000
    
    return {
        "total_raised": total_raised,
        "monthly_goal": GOAL,
        "progress_percentage": min(round((total_raised / GOAL) * 100, 1), 100),
        "active_initiatives": [
            {
                "id": 1,
                "name": "Community Education Fund",
                "description": "Scholarships for 50 underprivileged students",
                "target": 200000,
                "raised": total_raised * 0.4,
                "status": "In Progress"
            },
            {
                "id": 2,
                "name": "Emergency Medical Aid",
                "description": "Support for urgent surgeries and medication",
                "target": 150000,
                "raised": total_raised * 0.3,
                "status": "Active"
            },
            {
                "id": 3,
                "name": "Infrastructure Repair",
                "description": "Roof maintenance and hall renovation",
                "target": 150000,
                "raised": total_raised * 0.3,
                "status": "Planning"
            }
        ],
        "fund_allocation": {
            "Education": 40,
            "Medical": 30,
            "Infrastructure": 20,
            "Reserves": 10
        },
        "impact_message": "Your contributions are changing lives. Together, we are building a stronger, healthier community."
    }
