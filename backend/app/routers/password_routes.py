"""
Password change route for members who need to change their default password
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..db import members_collection
from ..auth import get_password_hash, verify_password
from ..dependencies import get_current_user

router = APIRouter()


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/change-password")
async def change_password(
    request: PasswordChangeRequest,
    current_user: dict = Depends(get_current_user)
):
    """Allow user to change their password"""
    # Verify current password
    if not verify_password(request.current_password, current_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Validate new password
    if len(request.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters")
    
    # Update password and remove must_change_password flag
    new_password_hash = get_password_hash(request.new_password)
    members_collection.update_one(
        {"email": current_user["email"]},
        {
            "$set": {
                "password_hash": new_password_hash,
                "must_change_password": False
            }
        }
    )
    
    return {"status": "success", "message": "Password changed successfully"}
