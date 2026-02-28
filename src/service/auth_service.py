from src.models.user import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.schema.user_schemas import SignUpRequest
from src.config.config import settings
from src.schema.login_schema import loginRequest, loginResponse
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify (plain_password, hashed_password)


class AuthService:
    """Service class for authentification related operations"""

    @staticmethod
    def hash_password(password:str)-> str:
        "Hashes password of a user"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"),salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def create_access_token(data: dict, expiration_time: Optional[timedelta] = None) -> str:
        data_to_encode = data.copy()

        if expiration_time:
            expires = datetime.now(timezone.utc) + expiration_time
        else:
            expires = datetime.now(timezone.utc) + timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRES
            )

        data_to_encode.update({"exp": expires, "type": "access"})

        encoded_jwt = jwt.encode(
            data_to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def refresh_token(data: dict, expiration_time: Optional[timedelta] = None) -> str:
        data_to_encode = data.copy()

        if expiration_time:
            expires = datetime.now(timezone.utc) + expiration_time
        else:
            expires = datetime.now(timezone.utc) + timedelta(
                minutes=settings.JWT_REFRESH_TOKEN_EXPIRES
            )

        data_to_encode.update({"exp": expires, "type": "refresh"})

        encoded_refresh_jwt = jwt.encode(
            data_to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_refresh_jwt


    @staticmethod
    def create_user(db:Session, user_data: SignUpRequest)-> User:
        """Register a new user in the database"""
        if  db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail ="Email already exists.")
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail ="Username already exists.")

        password_hash= AuthService.hash_password(user_data.password)

        new_user =User(
        email = user_data.email,
        username = user_data.username,
        password = password_hash,
        phone_no = user_data.phone,
        role = user_data.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


    @staticmethod
    def login(db: Session, login_detail: loginRequest) -> loginResponse:
        """Login a user and return token"""
        try:
            user = db.query(User).filter(User.email == login_detail.email).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            if not verify_password(login_detail.password, user.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            access_token = AuthService.create_access_token(data={"id": user.id, "sub": user.email, "role": user.role})
            refresh_token = AuthService.refresh_token(data={"sub": user.email, "role": user.role})
            return loginResponse(
                email = user.email,
                role = user.role,
                access_token = access_token,
                refresh_token = refresh_token
            )
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "internal server error")
            
        