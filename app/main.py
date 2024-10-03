from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor
import time

import psycopg2.extras
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


app = FastAPI()


for i in range(10):
    try:
        conn = psycopg2.connect(
            host='localhost', port='5432', user='postgres', 
            password='Daf28876#@', dbname='social-media-db', cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print("Database connection created successfully")
        break
    except psycopg2.Error as error:
        print("Connectin to database failed")
        print("ERROR: ", error)
        time.sleep(2)



class Post(BaseModel):
    id : Optional[uuid.UUID] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    datetime_created: Optional[datetime] = None



@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
async def get_posts():
    cursor.execute('''Select * From posts''')
    posts = cursor.fetchall()
    return {
        "message": "these are all of the posts",
        "data" : posts  
        }


@app.get("/posts/{id}")
async def get_post_by_id(id: uuid.UUID):
    print(type(id), id)
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!"
            )
    
    return {
    "message": f"post found with id: {id}",
    "data": post
}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(
        '''INSERT INTO posts (title, content, published) 
        VALUES (%s, %s, %s) RETURNING *
        ''' , (post.title, post.content, post.published)
        )
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "message": "post created successfully",
        "data": new_post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: uuid.UUID):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
async def update_post_by_id(id: uuid.UUID, post: Post):
    cursor.execute(
        '''UPDATE posts SET title = %s, content = %s, published = %s 
        WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id))
        )
    
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found"
        )
    
    conn.commit()
    return {
        "message": "Post Updated Succesfully",
        "data": updated_post
    }








