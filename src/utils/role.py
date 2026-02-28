from fastapi import Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from  fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config.database import get_db
from src.models.user import User
from src.config.config import settings
import jwt


security = HTTPBearer()



def get_current_user(request:Request, credentials: HTTPAuthorizationCredentials= Depends(security), db: Session = Depends(get_db)) -> User:

    """verifies the validity of the token of current user and returns the user object"""
    try:
        token = credentials.credentials
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token is missing"
            )
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user id not found"
            )

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )



def role_required(allowed_roles: list):
    """Dependency to state which roles are allowed to access a particular route"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return current_user
    return role_checker
