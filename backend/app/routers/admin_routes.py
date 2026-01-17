"""
Admin routes for the Contribution Tracking API.
Handles admin dashboard, member management, ticket management, and notifications.
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import Optional

from ..db import (
    members_collection,
    contributions_collection,
    notifications_collection,
    tickets_collection,
    admins_collection
)
from ..models import MemberCreate
from ..dependencies import require_admin
from ..utilities import (
    calculate_delay_days,
    classify_member,
    validate_phone,
    validate_email,
    generate_employee_id,
    generate_member_id,
    calculate_payment_status
)
from ..intelligence import IntelligenceEngine
from ..notifications import notification_engine

router = APIRouter()


from ..auth import get_password_hash

# ... (near the top of the file with other imports)

@router.post("/members")
async def register_member_admin(member: MemberCreate, admin: dict = Depends(require_admin)):
    """Admin: Register a new member with auto-generated member ID, employee ID, and default password"""
    
    # Auto-generate member_id if not provided
    if not member.member_id:
        member.member_id = generate_member_id()
    
    # Check if member_id already exists
    if members_collection.find_one({"member_id": member.member_id}):
        raise HTTPException(status_code=400, detail="Member ID already exists")
    
    if not validate_phone(member.phone):
        raise HTTPException(status_code=400, detail="Invalid phone number. Must be 10 digits.")
    
    if member.email and not validate_email(member.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    employee_id = generate_employee_id()
    
    # Use default values if not provided (₹500 on 5th)
    monthly_amount = member.monthly_amount if member.monthly_amount else 500
    due_day = member.due_day if member.due_day else 5
    
    # Set default password "pass123" that must be changed on first login
    default_password_hash = get_password_hash("pass123")
    
    member_data = {
        "member_id": member.member_id,
        "employee_id": employee_id,
        "name": member.name,
        "phone": member.phone,
        "email": member.email,
        "password_hash": default_password_hash,
        "must_change_password": True,
        "monthly_amount": monthly_amount,
        "due_day": due_day,
        "role": "member",
        "created_at": datetime.now(),
        "notification_preferences": {
            "email": True,
            "sms": False,
            "whatsapp": False,
            "reminder_days_before": 3
        }
    }
    
    members_collection.insert_one(member_data)
    return {
        "status": "success",
        "message": "Member registered with default password 'pass123'",
        "member_id": member.member_id,
        "employee_id": employee_id,
        "default_password": "pass123"
    }


@router.get("/members")
async def get_all_members_admin(admin: dict = Depends(require_admin)):
    """Admin: Get all members with statistics"""
    members = []
    
    for member in members_collection.find():
        contributions = list(contributions_collection.find({"member_id": member["member_id"]}))
        
        total_contributions = len(contributions)
        paid_count = sum(1 for c in contributions if c.get("paid_date"))
        missed_count = total_contributions - paid_count
        
        delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
                  for c in contributions if c.get("paid_date")]
        avg_delay = sum(delays) / len(delays) if delays else 0
        
        unpaid_contributions = [c for c in contributions if not c.get("paid_date")]
        current_delay = max([calculate_delay_days(c["due_date"]) 
                           for c in unpaid_contributions], default=0)
        
        classification = classify_member(missed_count, avg_delay)
        
        # Determine priority for proactive fund collection
        priority = "Early Reminder" if classification == "High-risk Delay" else "Normal"
        
        members.append({
            "member_id": member["member_id"],
            "employee_id": member.get("employee_id", "N/A"),
            "name": member["name"],
            "phone": member["phone"],
            "email": member.get("email"),
            "monthly_amount": member["monthly_amount"],
            "due_day": member["due_day"],
            "total_contributions": total_contributions,
            "paid_count": paid_count,
            "missed_count": missed_count,
            "avg_delay_days": round(avg_delay, 1),
            "current_delay_days": current_delay,
            "classification": classification,
            "priority": priority,
            "active": True
        })
    return members


@router.patch("/members/{member_id}/payment-settings")
async def update_member_payment_settings(
    member_id: str,
    monthly_amount: float,
    due_day: int,
    admin: dict = Depends(require_admin)
):
    """Admin: Update member's monthly amount and due day"""
    if due_day < 1 or due_day > 31:
        raise HTTPException(status_code=400, detail="Due day must be between 1 and 31")
    
    result = members_collection.update_one(
        {"member_id": member_id},
        {"$set": {
            "monthly_amount": monthly_amount,
            "due_day": due_day
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return {
        "status": "success",
        "message": "Payment settings updated",
        "member_id": member_id,
        "monthly_amount": monthly_amount,
        "due_day": due_day
    }


@router.get("/tickets")
async def get_all_tickets_admin(
    status_filter: Optional[str] = None,
    admin: dict = Depends(require_admin)
):
    """Admin: Get all tickets with optional status filter"""
    query = {}
    if status_filter and status_filter in ["pending", "approved", "rejected"]:
        query["status"] = status_filter
    
    tickets = list(tickets_collection.find(query).sort("created_at", -1))
    
    result = []
    for t in tickets:
        member = members_collection.find_one({"member_id": t["member_id"]})
        result.append({
            "ticket_id": t["ticket_id"],
            "member_id": t["member_id"],
            "member_name": member["name"] if member else "Unknown",
            "employee_id": t["employee_id"],
            "request_type": t["request_type"],
            "reason": t["reason"],
            "current_value": t["current_value"],
            "new_value": t["new_value"],
            "status": t["status"],
            "created_at": t["created_at"],
            "updated_at": t.get("updated_at"),
            "admin_response": t.get("admin_response")
        })
    
    return result


@router.patch("/{ticket_id}")
async def update_ticket_status(
    ticket_id: str,
    status: str,
    admin_response: Optional[str] = None,
    admin: dict = Depends(require_admin)
):
    """Admin: Approve or reject a ticket"""
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")
    
    ticket = tickets_collection.find_one({"ticket_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    tickets_collection.update_one(
        {"ticket_id": ticket_id},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.now(),
                "admin_response": admin_response
            }
        }
    )
    
    if status == "approved":
        update_field = {ticket["request_type"]: ticket["new_value"]}
        members_collection.update_one(
            {"member_id": ticket["member_id"]},
            {"$set": update_field}
        )
    
    return {
        "status": "success",
        "message": f"Ticket {status}",
        "ticket_id": ticket_id
    }


@router.get("/search")
async def search_members_by_employee_id(
    employee_id: str,
    admin: dict = Depends(require_admin)
):
    """Admin: Search for members by employee ID"""
    member = members_collection.find_one({"employee_id": employee_id})
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    contributions = list(contributions_collection.find({"member_id": member["member_id"]}))
    total_contributions = len(contributions)
    paid_count = sum(1 for c in contributions if c.get("paid_date"))
    missed_count = total_contributions - paid_count
    
    delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
              for c in contributions if c.get("paid_date")]
    avg_delay = sum(delays) / len(delays) if delays else 0
    
    unpaid_contributions = [c for c in contributions if not c.get("paid_date")]
    current_delay = max([calculate_delay_days(c["due_date"]) 
                       for c in unpaid_contributions], default=0)
    
    classification = classify_member(missed_count, avg_delay)
    
    return {
        "member_id": member["member_id"],
        "employee_id": member.get("employee_id", "N/A"),
        "name": member["name"],
        "phone": member["phone"],
        "email": member.get("email"),
        "monthly_amount": member["monthly_amount"],
        "due_day": member["due_day"],
        "total_contributions": total_contributions,
        "paid_count": paid_count,
        "missed_count": missed_count,
        "avg_delay_days": round(avg_delay, 1),
        "current_delay_days": current_delay,
        "classification": classification,
        "status": "Active"
    }


@router.get("/dashboard/stats")
async def get_dashboard_stats_admin(admin: dict = Depends(require_admin)):
    """Admin: Dashboard statistics with predictions"""
    total_members = members_collection.count_documents({})
    
    all_contributions = list(contributions_collection.find())
    total_contributions = len(all_contributions)
    paid_contributions = sum(1 for c in all_contributions if c.get("paid_date"))
    unpaid_contributions = total_contributions - paid_contributions
    
    total_collected = sum((c.get("amount") or 0) for c in all_contributions if c.get("paid_date"))
    total_pending = sum((c.get("amount") or 0) for c in all_contributions if not c.get("paid_date"))
    
    # Current month
    current_month = datetime.now().strftime("%Y-%m")
    monthly_contributions = [c for c in all_contributions if c["due_date"].startswith(current_month)]
    monthly_paid = sum(1 for c in monthly_contributions if c.get("paid_date"))
    monthly_collected = sum((c.get("amount") or 0) for c in monthly_contributions if c.get("paid_date"))
    
    # High-risk count
    high_risk_count = 0
    for member in members_collection.find():
        contributions = list(contributions_collection.find({"member_id": member["member_id"]}))
        missed_count = sum(1 for c in contributions if not c.get("paid_date"))
        delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
                  for c in contributions if c.get("paid_date")]
        avg_delay = sum(delays) / len(delays) if delays else 0
        
        if classify_member(missed_count, avg_delay) == "High-risk Delay":
            high_risk_count += 1
    
    return {
        "total_members": total_members,
        "total_contributions": total_contributions,
        "paid_contributions": paid_contributions,
        "unpaid_contributions": unpaid_contributions,
        "total_collected": round(total_collected, 2),
        "total_pending": round(total_pending, 2),
        "current_month": {
            "month": current_month,
            "total_contributions": len(monthly_contributions),
            "paid_contributions": monthly_paid,
            "collected_amount": round(monthly_collected, 2)
        },
        "high_risk_members": high_risk_count
    }


from pydantic import BaseModel

class ReminderRequest(BaseModel):
    custom_message: Optional[str] = None

@router.post("/reminders/{member_id}")
async def send_manual_reminder(member_id: str, request: ReminderRequest = None, admin: dict = Depends(require_admin)):
    """Admin: Manually send reminder to a member (optionally with custom message)"""
    member = members_collection.find_one({"member_id": member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    contributions = list(contributions_collection.find({"member_id": member_id}))
    
    # Find next unpaid contribution
    unpaid = [c for c in contributions if not c.get("paid_date")]
    
    # Logic: Only block if NO custom message AND no unpaid dues (nothing to remind about)
    if not unpaid and not (request and request.custom_message):
        return {"status": "info", "message": "No unpaid contributions"}
    
    # Determine due date string for email
    if unpaid:
        next_due = min(unpaid, key=lambda x: x["due_date"])
        due_date_str = next_due["due_date"]
        due_date_obj = datetime.strptime(due_date_str, "%Y-%m-%d")
    else:
        due_date_str = "No Pending Dues"
        due_date_obj = datetime.now()

    # Use custom message if provided, else generate one
    if request and request.custom_message:
        message = request.custom_message
    else:
        # Generate reminder (Requires unpaid dues to work correctly)
        if not unpaid:
             return {"status": "info", "message": "No unpaid contributions to generate reminder for"}

        prediction = IntelligenceEngine.predict_delay_likelihood(contributions, member)
        missed_count = len(unpaid)
        delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
                  for c in contributions if c.get("paid_date")]
        avg_delay = sum(delays) / len(delays) if delays else 0
        classification = classify_member(missed_count, avg_delay)
        
        days_until = (due_date_obj - datetime.now()).days
        
        message = IntelligenceEngine.generate_adaptive_reminder(
            member, classification, prediction, days_until
        )
    
    # Always create a dashboard notification
    notifications_collection.insert_one({
        "member_id": member_id,
        "notification_type": "reminder",
        "sent_at": datetime.now(),
        "message": message,
        "status": "sent"
    })

    # Send email if enabled
    prefs = member.get("notification_preferences", {})
    results = []
    
    if prefs.get("email") and member.get("email"):
        html_body = notification_engine.generate_email_html(
            member["name"], message, 
            member["monthly_amount"], due_date_str
        )
        result = await notification_engine.send_email(
            member["email"],
            "Contribution Reminder",
            message,
            html_body
        )
        results.append(result)
        # Note: We track the main notification above. Audit log could be separate if needed.
    
    return {"status": "success", "notifications_sent": len(results), "results": results}


@router.post("/contributions/generate")
async def generate_monthly_contributions(admin: dict = Depends(require_admin)):
    """
    Generate monthly contributions for all members
    This creates contribution records for the current month if they don't exist yet
    Now also sends automated reminder emails with statistics to all members!
    """
    from datetime import datetime
    from ..utilities import calculate_delay_days, classify_member
    from ..intelligence import IntelligenceEngine
    from ..notifications import notification_engine
    import calendar
    
    # Get current year and month
    now = datetime.now()
    current_month = f"{now.year}-{now.month:02d}"
    
    # Calculate due date (10th of current month)
    due_date = f"{now.year}-{now.month:02d}-10"
    
    # Check if contributions for this month already exist
    existing_count = contributions_collection.count_documents({"month": current_month})
    
    if existing_count > 0:
        return {
            "status": "already_exists",
            "message": f"Contributions for {current_month} already exist ({existing_count} contributions)",
            "month": current_month,
            "due_date": due_date
        }
    
    # Get all members (exclude admins)
    members = list(members_collection.find({"role": "member"}))
    
    if not members:
        return {
            "status": "no_members",
            "message": "No members found to generate contributions for",
            "month": current_month
        }
    
    # Create contributions
    contributions_to_insert = []
    for member in members:
        contribution = {
            "member_id": member["member_id"],
            "due_date": due_date,
            "amount": member.get("monthly_amount", 500),  # Use member's monthly_amount or default to 500
            "paid_date": None,
            "month": current_month,  # For easy querying
            "status": "pending"
        }
        contributions_to_insert.append(contribution)
    
    # Insert all contributions
    result = contributions_collection.insert_many(contributions_to_insert)
    
    # 📧 NEW: Send automated reminder emails to all members with statistics
    emails_sent = 0
    emails_skipped = 0
    email_errors = 0
    
    for member in members:
        try:
            member_id = member["member_id"]
            member_name = member["name"]
            
            # Calculate member's statistics
            all_contributions = list(contributions_collection.find({"member_id": member_id}))
            total_contributions = len(all_contributions)
            paid_count = sum(1 for c in all_contributions if c.get("paid_date"))
            missed_count = total_contributions - paid_count
            
            # Calculate classification
            delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
                     for c in all_contributions if c.get("paid_date")]
            avg_delay = sum(delays) / len(delays) if delays else 0
            classification = classify_member(missed_count, avg_delay)
            
            # Calculate days until due
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            days_until = (due_date_obj - datetime.now()).days
            
            # Generate personalized adaptive reminder message
            prediction = IntelligenceEngine.predict_delay_likelihood(all_contributions, member)
            message = IntelligenceEngine.generate_adaptive_reminder(
                member, classification, prediction, days_until
            )
            
            # Add context about monthly generation
            if classification == "High-risk Delay":
                message += "\n\n⚡ We're reaching out early to help you plan ahead for this month's contribution."
            else:
                message += "\n\n✨ This month's contribution has been generated. Thank you for your continued support!"
            
            # Check if member has email configured
            prefs = member.get("notification_preferences", {})
            if prefs.get("email") and member.get("email"):
                # Generate enhanced email with statistics
                html_body = notification_engine.generate_email_with_stats(
                    member_name, message,
                    member.get("monthly_amount", 500), due_date,
                    total_contributions, paid_count, missed_count,
                    classification
                )
                
                # Send email
                email_result = await notification_engine.send_email(
                    member["email"],
                    f"📅 {current_month} Contribution Generated",
                    message,
                    html_body
                )
                
                if email_result.get("status") == "sent":
                    emails_sent += 1
                else:
                    email_errors += 1
            else:
                emails_skipped += 1
                
        except Exception as e:
            # Assuming 'logger' is imported elsewhere or needs to be added
            # from loguru import logger # Example import
            # logger.error(f"Error sending email to {member.get('name', 'unknown')}: {str(e)}")
            print(f"Error sending email to {member.get('name', 'unknown')}: {str(e)}") # Fallback print
            email_errors += 1
            continue
    
    return {
        "status": "success",
        "message": f"Generated {len(result.inserted_ids)} contributions for {current_month}",
        "month": current_month,
        "due_date": due_date,
        "contributions_created": len(result.inserted_ids),
        "emails_sent": emails_sent,
        "emails_skipped": emails_skipped,
        "email_errors": email_errors
    }


# ============================================================================
# AUTOMATED REMINDER MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/reminders/schedule")
async def get_reminder_schedule(admin: dict = Depends(require_admin)):
    """Get the current automated reminder schedule configuration"""
    from ..scheduler import scheduler
    
    if scheduler is None:
        return {
            "status": "inactive",
            "message": "Scheduler has not been initialized"
        }
    
    if not scheduler.running:
        return {
            "status": "inactive",
            "message": "Scheduler is not running"
        }
    
    jobs = scheduler.get_jobs()
    reminder_job = next((job for job in jobs if job.id == 'daily_reminder_check'), None)
    
    if not reminder_job:
        return {
            "status": "not_scheduled",
            "message": "No reminder job found"
        }
    
    return {
        "status": "active",
        "schedule": "Daily at 9:00 AM",
        "next_run": reminder_job.next_run_time.isoformat() if reminder_job.next_run_time else None,
        "job_id": reminder_job.id,
       "timezone": str(scheduler.timezone),
        "reminder_policy": {
            "high_risk": "7 days before due date",
            "regular": "3 days before due date"
        }
    }



@router.post("/reminders/trigger")
async def trigger_reminder_check(admin: dict = Depends(require_admin)):
    """Manually trigger the automated reminder check (for testing/immediate execution)"""
    from ..scheduler import check_and_send_reminders
    
    result = await check_and_send_reminders()
    
    return {
        "message": "Reminder check triggered manually",
        "result": result,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/reminders/history")
async def get_reminder_history(limit: int = 50, admin: dict = Depends(require_admin)):
    """Get recent automated reminder sending history"""
    
    # Get recent reminders from notifications collection
    reminders = list(notifications_collection.find(
        {"notification_type": "reminder"},
        {"_id": 0}
    ).sort("sent_at", -1).limit(limit))
    
    # Convert datetime objects to ISO strings for JSON serialization
    for reminder in reminders:
        if isinstance(reminder.get("sent_at"), datetime):
            reminder["sent_at"] = reminder["sent_at"].isoformat()
    
    # Calculate statistics
    high_risk_count = sum(1 for r in reminders if r.get("priority") == "Early Reminder")
    regular_count = sum(1 for r in reminders if r.get("priority") == "Normal")
    
    return {
        "total": len(reminders),
        "statistics": {
            "high_risk_reminders": high_risk_count,
            "regular_reminders": regular_count
        },
        "reminders": reminders
    }
