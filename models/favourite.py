from models.base import Base
from sqlalchemy import TEXT, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

class Favourite(Base):
    __tablename__ = 'favourites'
    
    id = Column(TEXT, primary_key=True)
    podcast_id = Column(TEXT, ForeignKey('podcasts.id'))
    user_id = Column(TEXT, ForeignKey('users.id'))
    
    podcast = relationship('Podcast')
    user = relationship('User', back_populates='favourites')
    