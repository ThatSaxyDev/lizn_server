import os
import uuid
import bcrypt
from fastapi import Depends, HTTPException, APIRouter, Header
import jwt
from sqlalchemy.orm import Session
from database import get_db
from exception import CustomHTTPException
from middleware.auth_middleware import auth_middleware
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
from response import login_success_response, success_response
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload

router = APIRouter()

# Load environment variables
load_dotenv()

# sign up route
@router.post('/signup', status_code=201)  
def signup_user(user: UserCreate, db: Session=Depends(get_db)):
    # check if user exists in the db
    user_db = db.query(User).filter(User.email == user.email).first()
    
    if user_db: 
        raise CustomHTTPException(
            status_code=400,
            message="User with the same email already exists"
        )
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt(16))
     
    user_db = User(id=str(uuid.uuid4()), email=user.email, password=hashed_password, name=user.name)
    
    # add user to db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    print(user_db.email)
    
    return success_response(user_db, status_code=201)


# log in route
@router.post('/login')
def login_user(user: UserLogin, db: Session=Depends(get_db)):
    # check if user exists in the db
    user_db = db.query(User).filter(User.email == user.email).first()
    
    if not user_db:
        raise CustomHTTPException(
            status_code=400,
            message="User with this email does not exist, please sign up"
        )
        
    # password matching or not
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password) 
    
    if not is_match:
        raise CustomHTTPException(
            status_code=400,
            message="Invalid credentials"
        )
    
    password_key = os.getenv('PASSWORD_KEY')
    token = jwt.encode({'id': user_db.id}, password_key)
    
    return login_success_response(user_db, token)


#
@router.get('/')
def current_user_data(db: Session=Depends(get_db), 
                      user_dict= Depends(auth_middleware)):
    user_db =  db.query(User).filter(User.id == user_dict['uid']).options(
        joinedload(User.favourites)).first()
    
    if not user_db:
        raise CustomHTTPException(
            status_code=404,
            message="User not found"
        )
        
    return login_success_response(user_db, user_dict['token'])