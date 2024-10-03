from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body


from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid



app = FastAPI()




class Post(BaseModel):
    id : Optional[uuid.UUID] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    datetime_created: Optional[datetime] = None




temp_posts = [
    {
        "id": uuid.UUID("2ac9fe60-c9f9-41c0-a984-d09fd703c729"), 
        "title": "post1", 
        "content": "post1 content",
        "datetime_created": "2024-10-03T18:08:54.148349"
    },
    {
    "id": uuid.UUID("42de2c20-8f56-4e5d-9000-3784baa9312d"),
    "title": "top beaches in egypt",
    "content": "alex, blue-lagoan and sa7el",
    "published": True,
    "rating": 5,
    "datetime_created": "2024-10-03T15:54:09.135676"
    }
]


def find_post(id: uuid.UUID):
    for post in temp_posts:
        if post["id"] == id:
            return post
    
def find_index_post(id: uuid.UUID):
    for index, post in enumerate(temp_posts):
        if post["id"] == id:
            return index
        
def update_post(index: int, id: uuid.UUID, post: dict) -> dict:
    updated_post = temp_posts[index]
    updated_post["title"] = post["title"]
    updated_post["content"] = post["content"]
    temp_posts[index] = updated_post
    return updated_post

        
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found"
            )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "message": f"post with id: {id} was not found"
        # }

    return {
    "message": f"post found with id: {id}",
    "data": post
}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = uuid.uuid4()
    post_dict["datetime_created"] = datetime.now()

    temp_posts.append(post_dict)
    return {
        "message": f"post created successfully with id: {post.id}",
        "data": post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: uuid.UUID):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} not found"
        )
    temp_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
async def update_post_by_id(id: uuid.UUID, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found"
        )
    post_dict = post.model_dump()
    updated_post = update_post(index, id, post_dict)

    return {
        "message": "Post Updated Succesfully",
        "data": updated_post
    }







