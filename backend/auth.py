from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Shop
from utils import hash_password, verify_password, create_token
from schemas import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    shop = Shop(name=payload.shop_name, subscription_active=False)
    db.add(shop)
    db.commit()
    db.refresh(shop)

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="admin",
        shop_id=shop.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token({"user_id": user.id, "shop_id": shop.id})

    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "shop_id": user.shop_id
        },
        "shop": {
            "id": shop.id,
            "name": shop.name,
            "subscription_active": shop.subscription_active
        }
    }

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_token({"user_id": user.id, "shop_id": user.shop_id})

    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "shop_id": user.shop_id
        }
    }
