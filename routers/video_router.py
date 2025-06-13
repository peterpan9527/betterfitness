from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from schemas import VideoCreate, VideoOut
from controller.video_controller import upload_video, list_videos, get_video, add_view_count, search_videos_by_query
from secure.jwt import get_current_user
from database import get_db
import logging

logger = logging.getLogger(__name__)

# 建立路由器
router = APIRouter(prefix="/videos", tags=["videos"])

# 上傳影片端點
@router.post("/upload", response_model=VideoOut)
async def upload(
    file: UploadFile = File(...),
    video: VideoCreate = Depends(),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上傳影片
    Args:
        file: 上傳的檔案
        video: 影片創建資料
        user: 當前使用者
        db: 資料庫 Session
    Returns:
        創建的影片資料
    """
    return await upload_video(file, video, user["sub"], db)

# 取得影片列表端點
@router.get("/", response_model=list[VideoOut])
def get_videos(db: Session = Depends(get_db)):
    """
    取得所有影片
    Args:
        db: 資料庫 Session
    Returns:
        影片列表
    """
    return list_videos(db)

# 取得單一影片端點
@router.get("/{video_id}", response_model=VideoOut)
def get_video_by_id(video_id: int, db: Session = Depends(get_db)):
    """
    根據 ID 取得影片
    Args:
        video_id: 影片 ID
        db: 資料庫 Session
    Returns:
        影片資料
    """
    return get_video(video_id, db)

# 增加播放次數端點
@router.post("/{video_id}/view")
def increment_view(video_id: int, db: Session = Depends(get_db)):
    """
    增加影片播放次數
    Args:
        video_id: 影片 ID
        db: 資料庫 Session
    Returns:
        更新後的播放次數
    """
    return add_view_count(video_id, db)

# 搜尋影片端點
@router.get("/search", response_model=list[VideoOut])
def search(query: str, db: Session = Depends(get_db)):
    """
    根據標題或上傳者搜尋影片
    Args:
        query: 搜尋關鍵字
        db: 資料庫 Session
    Returns:
        匹配的影片列表
    """
    return search_videos_by_query(query, db)