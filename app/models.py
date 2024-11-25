from sqlalchemy import Column, Boolean, Integer, String, Uuid, ForeignKey, Identity
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


from .database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, Identity(always=True, start=1, increment=1), primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    datetime_created =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    owner_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        
    owner = relationship("User", back_populates="posts")
    votes = relationship("Vote", back_populates="post")
    
class User(Base):
    __tablename__ = "users"
    id = Column(Uuid, primary_key=True, nullable=False, server_default=text('gen_random_uuid()'), index=True) 
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    datetime_created =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    
    posts = relationship("Post", back_populates="owner")
    votes = relationship("Vote", back_populates="user")
    
    
class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")
