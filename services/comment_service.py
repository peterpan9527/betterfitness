from sqlalchemy.orm import Session
from models import Comment
from schemas import CommentCreate
import logging

logger = logging.getLogger(__name__)

# 創建新留言
def create_comment(db: Session, comment: CommentCreate, video_id: int, user_id: int) -> Comment:
    """
    創建新留言
    Args:
        db: 資料庫 Session
        comment: 留言創建資料
        video_id: 影片 ID
        user_id: 使用者 ID
    Returns:
        創建的 Comment 物件
    """
    db_comment = Comment(content=comment.content, video_id=video_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    logger.info(f"Created comment for video {video_id} by user {user_id}")
    return db_comment

# 取得影片的所有留言
def get_comments_by_video_id(db: Session, video_id: int) -> list[Comment]:
    """
    取得某影片的所有留言
    Args:
        db: 資料庫 Session
        video_id: 影片 ID
    Returns:
        留言列表
    """
    comments = db.query(Comment).filter(Comment.video_id == video_id).all()
    logger.debug(f"Retrieved {len(comments)} comments for video {video_id}")
    return comments