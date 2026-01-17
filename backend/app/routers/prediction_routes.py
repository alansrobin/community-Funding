"""
Prediction routes for the Contribution Tracking API.
Handles predictive analytics and member insights.
"""
from fastapi import APIRouter, HTTPException, Depends

from ..db import members_collection, contributions_collection
from ..dependencies import require_admin
from ..intelligence import IntelligenceEngine

router = APIRouter()


@router.get("/")
async def get_predictions(admin: dict = Depends(require_admin)):
    """Admin: Get delay predictions for all members"""
    predictions = []
    
    for member in members_collection.find():
        contributions = list(contributions_collection.find({"member_id": member["member_id"]}))
        
        if len(contributions) < 2:
            continue
        
        prediction = IntelligenceEngine.predict_delay_likelihood(contributions, member)
        risk_score = IntelligenceEngine.calculate_risk_score(contributions, member)
        
        if prediction["will_delay"] or risk_score > 50:
            predictions.append({
                "member_id": member["member_id"],
                "member_name": member["name"],
                "risk_score": round(risk_score, 1),
                "will_delay": prediction["will_delay"],
                "estimated_delay_days": prediction["estimated_delay_days"],
                "confidence": round(prediction["confidence"], 2),
                "factors": prediction["factors"]
            })
    
    # Sort by risk score
    predictions.sort(key=lambda x: x["risk_score"], reverse=True)
    return predictions


@router.get("/{member_id}")
async def get_member_insights(member_id: str, admin: dict = Depends(require_admin)):
    """Admin: Get deep insights for a member"""
    member = members_collection.find_one({"member_id": member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    contributions = list(contributions_collection.find({"member_id": member_id}))
    insights = IntelligenceEngine.calculate_member_insights(member, contributions)
    
    return insights


@router.get("/insights/{member_id}")
async def get_member_insights_alt(member_id: str, admin: dict = Depends(require_admin)):
    """Admin: Get deep insights for a member (alternate endpoint for frontend compatibility)"""
    member = members_collection.find_one({"member_id": member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    contributions = list(contributions_collection.find({"member_id": member_id}))
    insights = IntelligenceEngine.calculate_member_insights(member, contributions)
    
    return insights
