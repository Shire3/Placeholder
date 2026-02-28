from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional


def success_response(status_code: int, message: str, data: Optional[Dict]=None):
    """Returnsa JSON responce for successful operations"""
    response_data={
    "status": "success",
    "message" : message,
    "data": data or {}
    }
    return JSONResponse(status_code=status_code, content=response_data)



def failure_response(status_code: int, message: str, data: Optional[Dict]=None):
    """Returnsa JSON responce for failed operations"""
    response_data={
    "status": "failure",
    "message" : message,
    "data": data or {}
    }
    return JSONResponse(status_code=status_code, content=response_data)