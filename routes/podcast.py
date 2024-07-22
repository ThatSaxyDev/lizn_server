import os
import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile
from database import get_db
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from middleware.auth_middleware import auth_middleware
from models.favourite import Favourite
from models.podcast import Podcast
from pydantic_schemas.favourite_podcast import FavouritePodcast
from response import success_response
from sqlalchemy.orm import joinedload



router = APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key=os.getenv('CLOUDINARY_API_KEY'), 
    api_secret=os.getenv('CLOUDINARY_API_SECRET'), 
    secure=True
)

# upload podcast
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

# get all podcasts
@router.get('/get-all-podcasts')
def list_podcasts(db: Session = Depends(get_db),
                  auth_dict = Depends(auth_middleware)):
    podcasts = db.query(Podcast).all()
    return {
        "message": f"{len(podcasts)} podcast(s) found" if podcasts else "No podcasts available",
        "podcasts": podcasts
    }
    
# favourite podcast
@router.post('/favourite-podcast')
def favourite_podcast(podcast: FavouritePodcast, 
                      db: Session = Depends(get_db), 
                      auth_dict = Depends(auth_middleware)):
    user_id = auth_dict['uid']
    
    fav_podcast = db.query(Favourite).filter(Favourite.podcast_id == podcast.podcast_id, Favourite.user_id == user_id).first()
    
    if fav_podcast:
        db.delete(fav_podcast)
        db.commit()
        return success_response('', message='Removed from favourites')
    else:
        new_fav = Favourite(id=str(uuid.uuid4()), podcast_id=podcast.podcast_id, user_id=user_id)
        db.add(new_fav)
        db.commit()
        return success_response('', message='Added to favourites')
    
# get a users favourite podcasts
@router.get('/get-favourite-podcasts')
def get_favourite_podcasts(db: Session = Depends(get_db), 
                    auth_dict = Depends(auth_middleware)):
    user_id = auth_dict['uid']
    
    fav_podcasts = db.query(Favourite).filter(Favourite.user_id == user_id).options(
        joinedload(Favourite.podcast)).all()
    
    return success_response(fav_podcasts, message=f"{len(fav_podcasts)} podcast(s) found" if fav_podcasts else "No podcasts available")
    