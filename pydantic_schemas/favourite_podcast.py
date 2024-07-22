from pydantic import BaseModel

class FavouritePodcast(BaseModel):
    podcast_id: str