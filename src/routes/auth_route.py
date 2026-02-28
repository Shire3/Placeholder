from src.service.auth_service import AuthService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.utils.response import success_response, failure_response
from src.schema.user_schemas import SignUpRequest
from src.schema.login_schema import loginRequest, loginResponse

auth_router = APIRouter()



@auth_router.post(
    path="/signup",
    response_model=dict,
    status_code=201,
    summary="Register a new user",
    description="This endpoint registers a new user into the system.",
    responses={
        201: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "User registered successfully",
                        "data": {
                            "id": 1,
                            "username": "pizzamonger",
                            "email": "zikabereyi@gmail.com",
                            "phone": "6539087423",
                            "role": "user"
                        }
                    }
                }
            }
        },
        409: {
            "description": "Conflict - Email or username or username already exists",
            "content": {
                "application/json": {
                    "example": {
                        "status": "failure",
                        "message": "Email or passward is invalid",
                        "data": {}
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "Content": {
                "application/json": {
                    "example": {
                        "status": "failure",
                        "message": "An unexpected error occured. Please try again later.",
                        "data": {}
                    }
                }
            }
        }
    }
    )

def sign_up(user_data: SignUpRequest, db: Session = Depends(get_db)):
    """Endpoint to register a new user"""

    try:
        new_user = AuthService.create_user(db, user_data)
        user_response = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "phone": new_user.phone_no,
            "role": new_user.role
        }
        return success_response(
            status_code=201,
            message="User registered successfully",
            data=user_response
        )

    except Exception as e:
        print(str(e))
        return failure_response(
            status_code=500,
            message="An unexpected error occurred. Please try again"
        )


@auth_router.post(
    path="/login",
    response_model=dict,
    status_code=201,
    summary="Login a user",
    description="This endpoint registers a new user into the system.",
    responses={
        201: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "User login successful",
                        "data": {
                            "id": 1,
                            "status": "Failure",
                            "access_token": "djghjlmjhgfdsdfghuytr",
                            "refresh_token": "fghjytfdfvbnjuytfvbnmkuyt",
                        }
                    }
                }
            }
        },
        409: {
            "description": "Conflict - Email or username or username already exists",
            "content": {
                "application/json": {
                    "example": {
                        "status": "failure",
                        "message": "Email already exists please chose a different mail address",
                        "data": {}
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": "failure",
                        "message": "An unexpected error occured. Please try again later.",
                        "data": {}
                    }
                }
            }
        }
    }
    )
def login_user(user_data: loginRequest, db:Session=Depends(get_db)):
    """Endpoint for generating access and refresh tokensr"""
    try:
        login = AuthService.login(db, user_data)
        return success_response(
            status_code=200,
            message="User login successfully",
            data= {"data":login.dict()}
        )
    except Exception as e:
        print(str(e))
        return failure_response(
            status_code=500,
            message="An unexpected error occurred. Please try again"
        )