from pydantic import BaseModel,EmailStr
#Pydantic schemas → “how data is sent/received through the API”.
#Schemas give you safe input validation + clean output control.

from typing import Optional

#Tenant Input
class TenantCreate(BaseModel):
    name: str
    plan: str = "Free"


# Return dict (or list of dicts) → FastAPI can JSON-serialize it directly → ✅ no orm_mode needed.

# Return SQLAlchemy object (or list of them) → FastAPI can’t serialize raw ORM objects → ✅ you need a Pydantic schema with orm_mode = True to “translate” them into JSON.


#Tenent Output
class Tenant(TenantCreate):
    id: int
    name:str
    class Config:
        orm_mode = True



class UserCreate(BaseModel):

    email:EmailStr
    password:str
    tenant :Optional [TenantCreate] =None

    is_admin: bool = False
    
    

# User Output
class User(BaseModel):
    id: int
    email:EmailStr
    tenant_id: Optional[int] = None

    is_admin :bool = False

    tenant: Optional[Tenant]
    

    class Config:
        orm_mode = True




# Combined schema for "Register company (tenant) + first admin user"
class TenantWithAdminCreate(BaseModel):
    tenant: TenantCreate
    admin: UserCreate


class ProjectCreate(BaseModel):
    title: str
    description: str



#Output
class Project(ProjectCreate):
    id: int
    tenant_id: int
    class Config:
        orm_mode = True



#Output fo Token
class Token(BaseModel):
    access_token: str
    token_type: str



#Output for login
class LoginRequest(BaseModel):
    email: str
    password: str
