import os
from fastapi import Header
import jwt
from exception import CustomHTTPException


def auth_middleware(x_auth_token=Header()):
    try:
        # get user token from headers
        if not x_auth_token:
            raise CustomHTTPException(
                status_code=401,
                message="No auth token, access denied!"
            )
            
        # decode token
        password_key = os.getenv('PASSWORD_KEY')
        verified_token = jwt.decode(x_auth_token, password_key, 'HS256')
        
        if not verified_token:
            raise CustomHTTPException(
                status_code=401,
                message="Token verification failed, authorization denied!"
            )
        
        # get ID from token
        uid = verified_token.get('id')
        return {'uid': uid, 'token': x_auth_token,}
    
    except jwt.PyJWTError:
        raise CustomHTTPException(
                status_code=401,
                message="Invalid token, authorization denied!"
            )