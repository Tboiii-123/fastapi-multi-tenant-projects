from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models
from database import SessionLocal
from auth import get_current_user
from fastapi.responses import JSONResponse


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/create", response_model=schemas.Project)
def create_project( project: schemas.ProjectCreate,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):

    # Ensure user is admin
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can create projects")

    # Ensure tenant exists
    tenant = db.query(models.Tenant).filter(models.Tenant.id == current_user.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Create project
    db_project = models.Project(
        title=project.title,
        description=project.description,
        tenant_id=current_user.tenant_id,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

@router.get("/{tenant_id}", response_model=list[schemas.Project])
def list_projects(tenant_id: int, db: Session = Depends(get_db),current_user: models.User= Depends(get_current_user)):

    
    project= db.query(models.Project).filter(models.Project.tenant_id == tenant_id).first()
    if  not current_user.is_admin:
         raise HTTPException(status_code=403, detail="Only admins can Check  projects")
    
    
    if  current_user.tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="You don't belong to this tenant")
    
    if  not project:
        raise HTTPException(status_code=403, detail="This project is'nt found in your Tenant")
    

    return db.query(models.Project).filter(models.Project.tenant_id == tenant_id).all()




@router.delete("/{tenant_id}/delete/{delete_id}", response_model =schemas.Tenant)
def delete_projects(tenant_id: int, delete_id: int , db:Session = Depends(get_db), current_user :models.User= Depends(get_current_user)):

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can have access to delete project")
    
    if current_user.tenant_id !=tenant_id:
        raise HTTPException(status_code=403, detail="You don't belong to this tenant")

    project =db.query(models.Project).filter(models.Project.tenant_id == tenant_id, models.Project.id == delete_id ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")


    db.delete(project)
    db.commit()

    
    content = {
        "message": "Project deleted successfully",
        "project": {
            "id": project.id,
            "title":project.title,
            "decription": project.description,
            
        },
    }

    return JSONResponse(content=content, status_code=200)




