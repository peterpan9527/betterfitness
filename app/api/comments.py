from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import CommentCreate, CommentOut
from models import Comment, Video
from database import get_db
from api.videos import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/{video_id}", response_model=CommentOut)
def create_comment(
    video_id: int,
    comment: CommentCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found")
    db_comment = Comment(content=comment.content, video_id=video_id, user_id=user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{video_id}", response_model=list[CommentOut])
def list_comments(video_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.video_id == video_id).all()
    return comments