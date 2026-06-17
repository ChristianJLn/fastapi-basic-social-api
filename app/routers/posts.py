from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import PostCreate, PostResponse, PostOut
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[PostOut], status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user),
              limit: int = 10, skip: int = 0, search: str = ""):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.id_post).label("votes")).join(models.Vote, models.Post.id == models.Vote.id_post, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).offset(skip).all()
    return posts
    #else:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/{post_id}", response_model=PostOut, status_code=status.HTTP_200_OK)
def get_post(post_id: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (post_id,))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.id_post).label("votes")).join(models.Vote, models.Post.id == models.Vote.id_post, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")

    return post

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        # cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s,%s,%s)""",
        #                (payload.title, payload.content, payload.published))
        # new_post = cursor.fetchone()
        # conn.commit()
        new_post = models.Post(owner_id= current_user.id, **payload.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post was not created")

@router.put("/{post_id}", response_model=PostResponse)
def edit_post(post_id:str, payload: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (payload.title, payload.content, payload.published, post_id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = update_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    elif updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to edit that Post")

    update_query.update(payload.model_dump(), synchronize_session=False)
    
    db.commit()

    return updated_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (post_id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_query = db.query(models.Post).filter(models.Post.id == post_id)
    deleted_post = deleted_query.first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    elif deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete that Post")

    deleted_query.delete(synchronize_session=False)
    db.commit()
    return {}
