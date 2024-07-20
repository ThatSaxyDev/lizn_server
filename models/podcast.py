from models.base import Base
from sqlalchemy import TEXT, VARCHAR, Column

class Podcast(Base):
    __tablename__ = 'songs'
    
    id = Column(TEXT, primary_key=True)
    podcast_url = Column(TEXT)
    thumbnail_url = Column(TEXT)
    podcast_name = Column(VARCHAR(100))
    creator = Column(TEXT)
    creator_id = Column(TEXT)
    hex_code = Column(VARCHAR(6))
    