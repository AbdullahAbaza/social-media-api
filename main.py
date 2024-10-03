from fastapi import FastAPI, Response, status
from fastapi.params import Body


from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid



app = FastAPI()




class Post(BaseModel):
    id : uuid.UUID = uuid.uuid4()
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    datetime_created: Optional[datetime] = datetime.now()




temp_posts = [
    {"id": uuid.UUID("2ac9fe60-c9f9-41c0-a984-d09fd703c729"), "title": "post1", "content": "post1 content"},
    {"id": uuid.UUID("75de8c59-739c-4577-b54f-2b9b9cfa90a8"), "title": "post2", "content": "post2 content"}
]


def find_post(id: uuid.UUID):
    for post in temp_posts:
        if post["id"] == id:
            return post
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
async def get_posts():
    return {
        "message": "these are all of the posts",
        "data" : temp_posts   
        }


@app.get("/posts/{id}")
async def get_post_by_id(id: uuid.UUID, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": f"post with id: {id} was not found"
        }
    return {
    "message": f"post found with id: {id}",
    "data": post
}



@app.post("/posts/create")
async def create_post(post: Post):
    post_dict = post.model_dump()
    temp_posts.append(post_dict)
    return {
        "message": f"post created successfully with id: {post.id}",
        "data": post
    }





