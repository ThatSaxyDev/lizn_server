import uuid
import bcrypt
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from exception import CustomHTTPException
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
from response import success_response

router = APIRouter()

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
    
    return success_response(user_db)