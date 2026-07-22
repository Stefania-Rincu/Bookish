from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as SessionType
from app.dependencies import get_db
from app.services.auth import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut

class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            response_model=UserOut,
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=Token,
        )

    def register(self, user: UserCreate, db: SessionType = Depends(get_db)) -> User:
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already registered",
            )
        db_user = User(
            last_name=user.last_name,
            first_name=user.first_name,
            username=user.username,
            password_hash=get_password_hash(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def login(self, form_data: OAuth2PasswordRequestForm = Depends(), db: SessionType = Depends(get_db)) -> Token:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

auth_controller = AuthController()
