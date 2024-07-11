import bcrypt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

app = FastAPI()

DATABASE_URL = 'postgresql://postgres:test1234@127.0.0.1:5432/lizn'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

db = SessionLocal()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    
Base = declarative_base() 

class   User(Base):
    __tablename__ = 'users'
    
    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100)) 
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

@app.post('/signup')  
def signup_user(user: UserCreate):
    # check if user exists in the db
    user_db = db.query(User).filter(User.email == user.email).first()
    
    if user_db:
        raise HTTPException(400, 'User with the same email already exists')
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt(16))
     
    user_db = User(id=str(uuid.uuid4()), email=user.email, password=hashed_password, name=user.name)
    
    # add user to db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    return user_db

Base.metadata.create_all(engine)