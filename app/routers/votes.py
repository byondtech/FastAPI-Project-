
from fastapi import Response, status, HTTPException, Depends,APIRouter
from httpx import post
import  app.models as models, app.schemas as schemas, app.utils as utils, app.oauth2 as oauth2,app.database as database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/vote",
    tags= ['Votes']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    #if post doesnot exist
    post_for_vote = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_for_vote:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Post with id {vote.post_id} not found')
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    vote_found = vote_query.first()
    if (vote.dir == 1):
        if vote_found:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"{current_user.id} has already voted the post with id {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added succesfully"}
    else:
        if not vote_found:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Post does not exist")
        vote_query.delete(synchronize_session= False)
        db.commit()
        return {"message": "successfully deleted vote"}
    
