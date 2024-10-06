from sqlalchemy import Column, Boolean, Integer, String, Uuid
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Uuid, primary_key=True, nullable=False, server_default=text('gen_random_uuid()'))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    datetime_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    

 