from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
import schemas, models
from database import SessionLocal
from database import get_db
from auth import get_current_user
from fastapi.responses import JSONResponse


router = APIRouter()



#User can also view All tenant's

@router.get("/list",response_model=list[schemas.Tenant])
def view_all_tenant(db: Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):
     if current_user:
          all_tenant =db.query(models.Tenant).all()
          return all_tenant
     
     else:
          raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User isn't  logged in yet"
        )


# -----------------------------
# Tenant Users. all users 
# -----------------------------

@router.get("/{tenant_id}/users", response_model=list[schemas.User])
def list_users_by_tenant(tenant_id: int, db: Session = Depends(get_db),current_user:models.User =Depends(get_current_user)):
    print("current User:",current_user) 
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if  not current_user.is_admin :
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin"
        )
    
    if current_user.tenant_id != tenant_id:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not allowed to view this tenant's users"
        )
    
         
    
    return db.query(models.User).filter(models.User.tenant_id == tenant_id).all()


# Add users to tenant
@router.post("/{tenant_id}/users/{user_id}" ,response_model =schemas.User)
def add_user_to_tenant(user_id:int , tenant_id:int ,db:Session= Depends(get_db), current_user :models.User = Depends(get_current_user)):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin"
        )
    
    if current_user.tenant_id != tenant_id:
          raise HTTPException(
        status_code=403,
        detail="You can only manage users for your own tenant"
    )

    

    # ✅ continue only if admin
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    user.tenant_id = tenant.id
    db.commit()
    db.refresh(user)
    content ={
         "message":"User added to tenant successfully",
         user:{
              "id":user.id,
              "email":user.email,
              "tenant":tenant
         }
    }
    return JSONResponse(
         content=content,
         status_code=200
    )





@router.delete("/{tenant_id}/users/{user_id}", response_model=schemas.User)
def remove_user_from_tenant(    user_id: int, tenant_id: int, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin"
        )

    if current_user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=403,
            detail="You can only manage users for your own tenant"
        )

    # find the user
    user = db.query(models.User).filter(models.User.id == user_id, models.User.tenant_id == tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in this tenant")

    # unlink user from tenant (or you could db.delete(user) if you want to remove completely)
    user.tenant_id = None  
    db.commit()
    db.refresh(user)

    return JSONResponse(
        content={
            "message": "User removed from tenant successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "tenant_id": user.tenant_id
            }
        },
        status_code=200
    )
