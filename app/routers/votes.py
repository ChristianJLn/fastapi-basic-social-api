from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import Vote
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: Vote, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.id_post).first()
    db_vote_query = db.query(models.Vote).filter(models.Vote.id_post == vote.id_post, models.Vote.id_user == current_user.id,)
    db_vote = db_vote_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.id_post} was not found")
    
    if vote.dir:
        if db_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Post with id {vote.id_post} already has a vote")
        new_vote = models.Vote(id_post= vote.id_post, id_user= current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Successfully added vote"}
    else:
        if not db_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        db_vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}



        
            
