from datetime import datetime
from typing import Text, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4 as uid

app = FastAPI()

posts = []

#Post model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

# Cuando visiten la ruta inicial
@app.get('/') 
def read_root():
    return {'Welcome': 'Bienvenido a mi API REST'}

# Obtener las publicaciones
@app.get('/posts')
def get_posts():
    return posts

# Para buscar una publicacion en la url
@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(404, "Post not found")

# Guarda la publicacion y la retorna
@app.post('/posts')
def save_post(post: Post):
    post.id = str(uid())
    posts.append(post.dict())
    return posts[-1]

# Eliminar una publicacion
@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for i, post in enumerate(posts):
        if post['id'] == post_id:
            posts.pop(i)
            return {"message": "Post deleted successfully"}

    raise HTTPException(404, "Post not found")

# Actualizar una publicacion
@app.put('/posts/{post_id}')
def update_post(post_id: str, updated_post: Post):
    for i, post in enumerate(posts):
        if post['id'] == post_id:
            posts[i]['title'] = updated_post.title
            posts[i]['author'] = updated_post.author
            posts[i]['content'] = updated_post.content
            return {"mensage": "Post updated successfully"}

    raise HTTPException(404, "Post not found")