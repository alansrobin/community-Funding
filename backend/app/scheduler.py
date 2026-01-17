"""
Automated Reminder Scheduler
Sends payment reminders to members based on their priority level.
High-risk members receive reminders 7 days before due date.
Regular members receive reminders 3 days before due date.
"""
from datetime import datetime, timedelta
from typing import Dict, List
import logging

from .db import members_collection, contributions_collection, notifications_collection
from .utilities import calculate_delay_days, classify_member
from .intelligence import IntelligenceEngine
from .notifications import notification_engine

# Configure logger
logger = logging.getLogger(__name__)

# Scheduler instance (lazy initialization)
scheduler = None


async def should_send_reminder(member: Dict, contribution: Dict, priority: str) -> bool:
    """
    Determine if a reminder should be sent based on priority and due date.
    
    Args:
        member: Member document
        contribution: Contribution document
        priority: "Early Reminder" or "Normal"
    
    Returns:
        bool: True if reminder should be sent
    """
    due_date_str = contribution["due_date"]
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    days_until_due = (due_date - datetime.now()).days
    
    # Don't send reminders for already paid contributions
    if contribution.get("paid_date"):
        return False
    
    # Don't send reminders for past due dates
    if days_until_due < 0:
        return False
    
    # Check if reminder was already sent recently
    recent_reminder = notifications_collection.find_one({
        "member_id": member["member_id"],
        "contribution_id": contribution.get("_id"),
        "notification_type": "reminder",
        "sent_at": {"$gte": datetime.now() - timedelta(days=2)}
    })
    
    if recent_reminder:
        logger.info(f"Skipping {member['name']} - Reminder already sent recently")
        return False
    
    # Send based on priority and days until due
    if priority == "Early Reminder":
        # High-risk: Send 7 days before
        return days_until_due == 7
    else:
        # Regular: Send 3 days before
        return days_until_due == 3


async def send_member_reminder(member: Dict, contribution: Dict, classification: str, priority: str) -> Dict:
    """
    Send a reminder to a specific member for a specific contribution.
    
    Args:
        member: Member document
        contribution: Contribution document
        classification: Member classification
        priority: Member priority level
    
    Returns:
        Dict: Result of reminder sending
    """
    try:
        member_id = member["member_id"]
        member_name = member["name"]
        due_date_str = contribution["due_date"]
        
        # Calculate prediction and days until due
        all_contributions = list(contributions_collection.find({"member_id": member_id}))
        prediction = IntelligenceEngine.predict_delay_likelihood(all_contributions, member)
        
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        days_until = (due_date - datetime.now()).days
        
        # Generate adaptive message
        message = IntelligenceEngine.generate_adaptive_reminder(
            member, classification, prediction, days_until
        )
        
        # Add priority context to message
        if priority == "Early Reminder":
            message += "\n\n⚡ Early reminder: We're reaching out in advance to help you plan ahead."
        
        # Create notification record
        notification_doc = {
            "member_id": member_id,
            "contribution_id": contribution.get("_id"),
            "notification_type": "reminder",
            "sent_at": datetime.now(),
            "message": message,
            "priority": priority,
            "days_before_due": days_until,
            "status": "sent"
        }
        notifications_collection.insert_one(notification_doc)
        
        # Send email if configured
        results = []
        prefs = member.get("notification_preferences", {})
        
        if prefs.get("email") and member.get("email"):
            # Calculate stats for this member
            all_contributions = list(contributions_collection.find({"member_id": member_id}))
            total_contributions = len(all_contributions)
            paid_count = sum(1 for c in all_contributions if c.get("paid_date"))
            missed_count = total_contributions - paid_count
            
            # Use enhanced email template with statistics
            html_body = notification_engine.generate_email_with_stats(
                member_name, message,
                member["monthly_amount"], due_date_str,
                total_contributions, paid_count, missed_count,
                classification
            )
            
            result = await notification_engine.send_email(
                member["email"],
                f"{'🔔 Early ' if priority == 'Early Reminder' else ''}Payment Reminder",
                message,
                html_body
            )
            results.append(result)
            logger.info(f"✅ Reminder sent to {member_name} ({priority}, {days_until} days before due)")
        else:
            logger.info(f"⏭️ Skipped {member_name} - Email not configured")
        
        return {
            "member_id": member_id,
            "member_name": member_name,
            "priority": priority,
            "days_until_due": days_until,
            "status": "sent",
            "channels": results
        }
    
    except Exception as e:
        logger.error(f"❌ Error sending reminder to {member.get('name', 'unknown')}: {str(e)}")
        return {
            "member_id": member.get("member_id"),
            "member_name": member.get("name"),
            "status": "failed",
            "error": str(e)
        }


async def check_and_send_reminders():
    """
    Main scheduler task: Check all members and send reminders based on priority.
    Runs daily at 9:00 AM.
    """
    logger.info("🔔 Starting automated reminder check...")
    
    sent_count = 0
    skipped_count = 0
    error_count = 0
    
    try:
        # Get all active members
        try:
            members = list(members_collection.find({"role": "member"}))
            logger.info(f"Checking {len(members)} members for reminders...")
        except Exception as db_error:
            logger.error(f"❌ Database connection error: {str(db_error)}")
            return {
                "status": "failed",
                "error": f"Database connection failed: {str(db_error)}",
                "timestamp": datetime.now().isoformat(),
                "note": "Will retry on next scheduled run"
            }
        
        for member in members:
            try:
                member_id = member["member_id"]
                
                # Get all unpaid contributions for this member
                unpaid_contributions = list(contributions_collection.find({
                    "member_id": member_id,
                    "paid_date": None
                }))
                
                if not unpaid_contributions:
                    continue
                
                # Calculate member classification
                all_contributions = list(contributions_collection.find({"member_id": member_id}))
                total_contributions = len(all_contributions)
                paid_count = sum(1 for c in all_contributions if c.get("paid_date"))
                missed_count = total_contributions - paid_count
                
                delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
                         for c in all_contributions if c.get("paid_date")]
                avg_delay = sum(delays) / len(delays) if delays else 0
                
                classification = classify_member(missed_count, avg_delay)
                priority = "Early Reminder" if classification == "High-risk Delay" else "Normal"
                
                # Check each unpaid contribution
                for contribution in unpaid_contributions:
                    if await should_send_reminder(member, contribution, priority):
                        result = await send_member_reminder(member, contribution, classification, priority)
                        if result["status"] == "sent":
                            sent_count += 1
                        else:
                            error_count += 1
                    else:
                        skipped_count += 1
            
            except Exception as e:
                logger.error(f"Error processing member {member.get('name', 'unknown')}: {str(e)}")
                error_count += 1
                continue
        
        logger.info(f"""
        ✅ Reminder check completed:
           - Sent: {sent_count}
           - Skipped: {skipped_count}
           - Errors: {error_count}
        """)
        
        return {
            "status": "completed",
            "sent": sent_count,
            "skipped": skipped_count,
            "errors": error_count,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"❌ Fatal error in reminder check: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "note": "Scheduler will retry on next scheduled run"
        }


def start_scheduler():
    """Initialize and start the reminder scheduler"""
    global scheduler
    try:
        # Lazy import to avoid circular dependency issues
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        
        # Initialize scheduler
        scheduler = AsyncIOScheduler()
        
        # Schedule daily reminder check at 9:00 AM
        scheduler.add_job(
            check_and_send_reminders,
            'cron',
            hour=9,
            minute=0,
            id='daily_reminder_check',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("✅ Scheduler initialized successfully - Daily reminders at 9:00 AM")
        
    except Exception as e:
        logger.error(f"❌ Failed to start scheduler: {str(e)}")


def stop_scheduler():
    """Stop the scheduler gracefully"""
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
