from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

import models, schemas
from database import get_db
from typing import Optional

def hash_password(password: str):
    return pwd_context.hash(password)

router = APIRouter()

SECRET_KEY = "12345"  
ALGORITHM = "HS256"

#This creates a password hashing context using Passlib’s CryptContext
#We are usng bcrypt for the algorithm we can use argon2, pbkdf2_sha256
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



# helper function to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta]  = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ------------------------------
# LOGIN endpoint → return JWT
# ------------------------------

@router.post("/login", response_model=schemas.Token)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user :
        raise HTTPException(status_code=401, detail="Invalid Email")
    
    elif not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token_expires = timedelta(hours=2)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}






@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = models.User(
        email=user.email,
        password=hash_password(user.password)
    )

     # if tenant info is provided, create tenant and make this user admin
    if user.tenant:
        new_tenant = models.Tenant(name=user.tenant.name, plan=user.tenant.plan)
        db.add(new_tenant)
        db.flush()  # 👈 ensures new_tenant.id is available

        new_user.tenant_id = new_tenant.id
        new_user.is_admin = True

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

