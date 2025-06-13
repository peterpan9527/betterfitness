from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import CommentCreate, CommentOut
from services.comment_service import create_comment, get_comments_by_video_id
from services.video_service import get_video_by_id
import logging

logger = logging.getLogger(__name__)

# 新增留言
def add_comment(video_id: int, comment: CommentCreate, user_id: int, db: Session) -> CommentOut:
    """
    新增留言到指定影片
    Args:
        video_id: 影片 ID
        comment: 留言創建資料
        user_id: 使用者 ID
        db: 資料庫 Session
    Returns:
        創建的留言資料
    Raises:
        HTTPException: 如果影片不存在
    """
    video = get_video_by_id(db, video_id)
    if not video:
        logger.warning(f"Video not found for comment: ID {video_id}")
        raise HTTPException(status_code=404, detail="Video not found")
    db_comment = create_comment(db, comment, video_id, user_id)
    return db_comment

# 取得留言
def list_comments(video_id: int, db: Session) -> list[CommentOut]:
    """
    取得某影片的所有留言
    Args:
        video_id: 影片 ID
        db: 資料庫 Session
    Returns:
        留言列表
    """
    comments = get_comments_by_video_id(db, video_id)
    return comments