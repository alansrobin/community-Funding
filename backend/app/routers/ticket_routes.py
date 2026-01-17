"""
Ticket system routes for the Contribution Tracking API.
Handles ticket creation and retrieval for members.
"""
from fastapi import APIRouter, Depends
from datetime import datetime
from bson import ObjectId

from ..db import members_collection, tickets_collection
from ..models import TicketCreate
from ..dependencies import get_current_user
from ..utilities import generate_employee_id

router = APIRouter()


@router.post("/")
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: dict = Depends(get_current_user)
):
    """Member: Create a ticket to request changes"""
    member_id = current_user["member_id"]
    employee_id = current_user.get("employee_id", "N/A")
    
    # Get current value
    current_value = current_user.get(ticket_data.request_type, 0)
    
    # Create ticket
    ticket = {
        "ticket_id": str(ObjectId()),
        "member_id": member_id,
        "employee_id": employee_id,
        "request_type": ticket_data.request_type,
        "reason": ticket_data.reason,
        "current_value": float(current_value),
        "new_value": float(ticket_data.new_value),
        "status": "pending",
        "created_at": datetime.now(),
        "updated_at": None,
        "admin_response": None
    }
    
    tickets_collection.insert_one(ticket)
    
    return {
        "status": "success",
        "message": "Ticket created successfully",
        "ticket_id": ticket["ticket_id"]
    }


@router.get("/")
async def get_member_tickets(current_user: dict = Depends(get_current_user)):
    """Member: Get all tickets created by the member"""
    member_id = current_user["member_id"]
    tickets = list(tickets_collection.find({"member_id": member_id}).sort("created_at", -1))
    
    return [{
        "ticket_id": t["ticket_id"],
        "employee_id": t["employee_id"],
        "request_type": t["request_type"],
        "reason": t["reason"],
        "current_value": t["current_value"],
        "new_value": t["new_value"],
        "status": t["status"],
        "created_at": t["created_at"],
        "updated_at": t.get("updated_at"),
        "admin_response": t.get("admin_response")
    } for t in tickets]


@router.get("/generate-employee-id")
async def generate_employee_id_endpoint():
    """Generate a new employee ID"""
    employee_id = generate_employee_id()
    return {"employee_id": employee_id}
