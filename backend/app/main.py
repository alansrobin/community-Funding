"""
Enhanced Contribution Tracking API - Main Application
Clean entry point with router registration only.
All routes are organized in the routers/ directory.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup: Initialize scheduler
    from .scheduler import start_scheduler
    start_scheduler()
    yield
    # Shutdown: Stop scheduler
    from .scheduler import stop_scheduler
    stop_scheduler()

# Import routers
from .routers import (
    auth_routes,
    member_routes,
    ticket_routes,
    contribution_routes,
    admin_routes,
    prediction_routes,
    password_routes
)

# Create FastAPI app with lifespan management
app = FastAPI(
    title="Enhanced Contribution Tracking API",
    version="2.0",
    description="Intelligent contribution tracking with predictive analytics and automated reminders",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes and tags
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(password_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(member_routes.router, prefix="/member", tags=["Member Dashboard"])
app.include_router(ticket_routes.router, prefix="/member/tickets", tags=["Tickets"])
app.include_router(contribution_routes.router, prefix="/contributions", tags=["Contributions"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(prediction_routes.router, prefix="/admin/predictions", tags=["Predictions"])

# Public endpoints
@app.get("/", tags=["Root"])
def root():
    """API Root - Welcome endpoint"""
    return {
        "message": "Enhanced Contribution Tracking API v2.0",
        "features": [
            "JWT Authentication",
            "Member & Admin Roles",
            "Predictive Analytics",
            "Multi-channel Notifications",
            "Ethical Reminder System",
            "Ticket Management"
        ],
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0"}


@app.get("/members", tags=["Public"])
async def get_all_members_public():
    """Get all members with statistics (public for demo)"""
    from .db import members_collection, contributions_collection
    from .utilities import calculate_delay_days, classify_member
    
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
            "status": "Active"
        })
    
    return members


@app.get("/dashboard/high-risk", tags=["Public"])
async def get_high_risk_members():
    """Get high-risk members (public for demo)"""
    from .db import members_collection, contributions_collection
    from .utilities import calculate_delay_days, classify_member
    
    high_risk_members = []
    
    for member in members_collection.find():
        contributions = list(contributions_collection.find({"member_id": member["member_id"]}))
        
        if len(contributions) < 2:
            continue
        
        total_contributions = len(contributions)
        paid_count = sum(1 for c in contributions if c.get("paid_date"))
        missed_count = total_contributions - paid_count
        
        delays = [calculate_delay_days(c["due_date"], c["paid_date"]) 
                  for c in contributions if c.get("paid_date")]
        avg_delay = sum(delays) / len(delays) if delays else 0
        
        classification = classify_member(missed_count, avg_delay)
        
        if classification == "High-risk Delay":
            unpaid_contributions = [c for c in contributions if not c.get("paid_date")]
            current_delay = max([calculate_delay_days(c["due_date"]) 
                               for c in unpaid_contributions], default=0)
            
            high_risk_members.append({
                "member_id": member["member_id"],
                "name": member["name"],
                "phone": member["phone"],
                "email": member.get("email"),
                "missed_payments": missed_count,
                "avg_delay_days": round(avg_delay, 1),
                "current_delay_days": current_delay,
                "classification": classification
            })
    
    return high_risk_members


@app.get("/reminders/{member_id}", tags=["Reminders"])
async def get_reminder_preview(member_id: str):
    """Get a preview of the ethical reminder for a member"""
    from fastapi import HTTPException
    from .db import members_collection, contributions_collection
    from .utilities import calculate_delay_days, classify_member
    from .intelligence import IntelligenceEngine
    from datetime import datetime
    
    member = members_collection.find_one({"member_id": member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    contributions = list(contributions_collection.find({"member_id": member_id}))
    
    # Calculate stats
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
    
    # Generate Message
    prediction = IntelligenceEngine.predict_delay_likelihood(contributions, member)
    
    days_until = 0
    if unpaid_contributions:
        next_due = min(unpaid_contributions, key=lambda x: x["due_date"])
        due_date = datetime.strptime(next_due["due_date"], "%Y-%m-%d")
        days_until = (due_date - datetime.now()).days
    else:
        # If all paid, assume next month
        days_until = 30
    
    message = IntelligenceEngine.generate_adaptive_reminder(
        member, classification, prediction, days_until
    )
    
    return {
        "member_id": member_id,
        "member_name": member["name"],
        "classification": classification,
        "missed_payments": missed_count,
        "delay_days": current_delay,
        "reminder_message": message
    }
