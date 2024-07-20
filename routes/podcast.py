import os
import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile
from database import get_db
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from middleware.auth_middleware import auth_middleware
from models.podcast import Podcast
from response import success_response



router = APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key=os.getenv('CLOUDINARY_API_KEY'), 
    api_secret=os.getenv('CLOUDINARY_API_SECRET'), 
    secure=True
)

@router.post('/upload', status_code=201)
def upload_podcast(podcast: UploadFile = File(...), 
                   thumbnail: UploadFile = File(...), 
                   creator: str = Form(...),
                   creator_id: str = Form(...),
                   podcast_name: str = Form(...),
                   hex_code: str = Form(...),
                   db: Session = Depends(get_db),
                   auth_dict = Depends(auth_middleware)
                   ):
    podcast_id = str(uuid.uuid4())
    podcast_res = cloudinary.uploader.upload(podcast.file, resource_type='auto', folder=f'podcasts/{podcast_id}')
    print(podcast_res['url'])
    thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type='image', folder=f'podcasts/{podcast_id}')
    print(thumbnail_res['url'])
    
    new_podcast = Podcast(
        id=podcast_id,
        podcast_url=podcast_res['url'],
        thumbnail_url=thumbnail_res['url'],
        podcast_name=podcast_name,
        creator=creator,
        creator_id=creator_id,
        hex_code=hex_code,
    )
    
    db.add(new_podcast)
    db.commit()
    db.refresh(new_podcast)
    
    return success_response(new_podcast, status_code=201, message='Podcast uploaded successfully') 