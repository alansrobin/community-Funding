"""
Contribution routes for the Contribution Tracking API.
Handles payment tracking, contribution records, and status management.
"""
from fastapi import APIRouter, HTTPException, Depends

from ..db import members_collection, contributions_collection
from ..models import PaymentSubmit
from ..dependencies import require_admin, get_current_user
from ..utilities import calculate_delay_days, get_payment_status
from datetime import datetime

router = APIRouter()


@router.get("/status")
async def get_contributions_status():
    """Get payment statuses for all contributions (public for demo)"""
    all_contributions = list(contributions_collection.find())
    
    result = []
    for contribution in all_contributions:
        member = members_collection.find_one({"member_id": contribution["member_id"]})
        if member:
            result.append({
                "member_id": member["member_id"],
                "member_name": member["name"],
                "due_date": contribution["due_date"],
                "amount": contribution["amount"],
                "paid_date": contribution.get("paid_date"),
                "status": get_payment_status(contribution),
                "delay_days": calculate_delay_days(contribution["due_date"], contribution.get("paid_date"))
            })
    
    return result


@router.post("/payment")
async def record_payment(payment: PaymentSubmit):
    """Record a payment for a contribution (admin or demo)"""
    result = contributions_collection.update_one(
        {"_id": payment.contribution_id},
        {"$set": {"paid_date": payment.paid_date}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    return {"status": "success", "message": "Payment recorded"}


@router.post("/pay-all")
async def pay_all_pending(current_user: dict = Depends(get_current_user)):
    """Mark all unpaid contributions as paid for the current member"""
    member_id = current_user.get("member_id")
    
    # Update all unpaid contributions for this member
    result = contributions_collection.update_many(
        {
            "member_id": member_id,
            "paid_date": None
        },
        {
            "$set": {
                "paid_date": datetime.now().strftime("%Y-%m-%d")
            }
        }
    )
    
    return {
        "status": "success",
        "message": "Successfully paid!",
        "contributions_paid": result.modified_count
    }


@router.get("/failed-payment-stats")
async def get_failed_payment_stats(current_user: dict = Depends(require_admin)):
    """Get failed payment statistics"""
    all_contributions = list(contributions_collection.find({"paid_date": None}))
    
    failed_payments = []
    members_affected = set()
    
    for contribution in all_contributions:
        delay_days = calculate_delay_days(contribution["due_date"])
        if delay_days > 30:
            failed_payments.append(contribution)
            members_affected.add(contribution["member_id"])
    
    total_failed = len(failed_payments)
    total_amount = sum(c["amount"] for c in failed_payments)
    
    # Recent failures (last 10)
    recent_failures = []
    for contribution in failed_payments[:10]:
        member = members_collection.find_one({"member_id": contribution["member_id"]})
        recent_failures.append({
            "member_name": member["name"] if member else "Unknown",
            "amount": contribution["amount"],
            "due_date": contribution["due_date"],
            "delay_days": calculate_delay_days(contribution["due_date"])
        })
    
    return {
        "total_failed": total_failed,
        "total_amount": round(total_amount, 2),
        "members_affected": len(members_affected),
        "recent_failures": recent_failures
    }

