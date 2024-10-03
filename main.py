from fastapi import FastAPI
from fastapi.params import Body


from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI()


class Post(BaseModel):
    id : uuid.uuid4 = uuid.uuid4()
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    datetime_created: Optional[datetime] = datetime.now()




temp_posts = [
    {"id": uuid.uuid4(), "title": "post1" , "content": "post1 content"},
    {"id": uuid.uuid4(), "title": "post2" , "content": "post2 content"}
]


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {
        "message": "these are all of the posts",
        "data" : temp_posts   
        }



@app.post("/posts/create")
async def create_post(post: Post):
    post_dict = post.dict()
    print(post_dict)
    temp_posts.append(post_dict)
    return {
        "messasge": f"post created successfully with id: {post.id}",
        "date": post
        }



