from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from model import Post

app = FastAPI()


class PostCreate(BaseModel):
    subject: str
    content: str


@app.post("/create")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(subject=post.subject, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/post/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not Found")
    return post


@app.get("/Post")
def get_all_Post(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.put("/update/{post_id}")
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.subject = post.subject
    db_post.content = post.content
    db.commit()
    return {"message": "Post updated successfully", "updated post": db_post}


@app.delete("/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully", "deleted post": db_post}
