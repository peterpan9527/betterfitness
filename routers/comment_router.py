from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import CommentCreate, CommentOut
from controller.comment_controller import add_comment, list_comments
from secure.jwt import get_current_user
from database import get_db
import logging

logger = logging.getLogger(__name__)

# 建立路由器
router = APIRouter(prefix="/comments", tags=["comments"])

# 新增留言端點
@router.post("/{video_id}", response_model=CommentOut)
def create_comment(
    video_id: int,
    comment: CommentCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    新增留言
    Args:
        video_id: 影片 ID
        comment: 留言創建資料
        user: 當前使用者
        db: 資料庫 Session
    Returns:
        創建的留言資料
    """
    return add_comment(video_id, comment, user["sub"], db)

# 取得留言端點
@router.get("/{video_id}", response_model=list[CommentOut])
def get_comments(video_id: int, db: Session = Depends(get_db)):
    """
    取得某影片的所有留言
    Args:
        video_id: 影片 ID
        db: 資料庫 Session
    Returns:
        留言列表
    """
    return list_comments(video_id, db)