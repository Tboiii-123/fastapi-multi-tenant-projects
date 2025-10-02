#ApiRouter lets us split our router into modules
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
import schemas, models
from database import SessionLocal
from passlib.context import CryptContext
from auth import get_current_user

router = APIRouter()

from database import get_db
from fastapi.responses import JSONResponse





#Profile of a User
@router.get("/profile", response_model=schemas.User)
def profile(current_user: models.User = Depends(get_current_user)):
    return current_user






# Delete User
@router.delete("/delete/{user_id}")
def delete_profile(user_id: int,current_user: models.User = Depends(get_current_user),db: Session = Depends(get_db), response_model=schemas.User):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if  current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this user Profile"
        )

    

    

    db.delete(user)
    db.commit()

    content = {
        "message": "User deleted successfully",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }

    return JSONResponse(content=content, status_code=200)





     
    