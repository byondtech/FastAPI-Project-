
from typing import  List, Optional

from sqlalchemy import func
import app.models as models
import app.schemas as schemas
from fastapi import Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
import app.oauth2 as oauth2


router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)
 
#posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#@router.get("/",response_model= List[schemas.Post])
@router.get("/",response_model= List[schemas.Postout])
def get_posts(db: Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user), limit : int = 10,skip: int =0, search : 
              Optional[str] = ""):
    
    posts = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter= True).group_by(models.Post.
    id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# create posts
@router.post("/",response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, response: Response,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s, %s, %s) RETURNING *""",(post.title,
    # post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() #commit changes to the database

    new_post= models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    response.status_code = status.HTTP_201_CREATED
    return new_post
    
        
#get a particular post by id
@router.get("/{id}",response_model= schemas.Postout)
def get_post(id:int, response: Response,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = posts = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter= True).group_by(models.Post.
    id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message":f"post with id {id} was not found"}
    
    return post

#delete posts by id
@router.delete("/{id}")
def delete_post(id : int,response: Response,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
   # cursor.execute("""DELETE FROM posts WHERE ID = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with {id} does not exist")
    response.status_code = status.HTTP_204_NO_CONTENT
    if post.owner_id != current_user.id : raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail=f"Not aurhorized to perform requested action")
    post_query.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)


#update post with id

@router.put("/{id}",response_model= schemas.Post)
def update_post(id : int, updated_post : schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s,content = %s, published =%s WHERE id =%s returning *""",(post.title,post.content,post.published, str(id)))
    #updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with {id} does not exist")
    if post.owner_id != current_user.id : raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail=f"Not aurhorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()

    return post_query.first()