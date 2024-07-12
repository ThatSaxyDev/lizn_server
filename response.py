from typing import Any, Dict

def success_response(data: Any, status_code: int = 200) -> Dict[str, Any]:
    return {
        "status": "success",
        "statusCode": status_code,
        "data": data
    }