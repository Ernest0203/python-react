from fastapi import APIRouter, HTTPException, status
from auth.models import UserRegister, UserLogin
from auth.auth_utils import hash_password, verify_password, create_access_token
from database import db

router = APIRouter()

@router.post("/register")
async def register(user: UserRegister):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    await db.users.insert_one({"email": user.email, "password": hashed_pw})
    return {"msg": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
