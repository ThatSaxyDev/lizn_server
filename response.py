from typing import Any, Dict

def success_response(data: Any, status_code: int = 200) -> Dict[str, Any]:
    return {
        "status": "success",
        "statusCode": status_code,
        "data": data
    }

def login_success_response(data: Any, token: str, status_code: int = 200) -> Dict[str, Any]:
    return {
        "status": "success",
        "statusCode": status_code,
        "token": token,
        "data": data
    }