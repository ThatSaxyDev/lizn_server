from fastapi import FastAPI
from exception import CustomHTTPException, custom_http_exception_handler
from routes import auth
from models.base import Base
from database import engine

app = FastAPI()

app.include_router(auth.router, prefix='/auth')
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)

Base.metadata.create_all(engine)