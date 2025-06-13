from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from schemas import VideoCreate, VideoOut
from services.video_service import create_video, get_videos, get_video_by_id, increment_view_count, search_videos
import os
import logging

logger = logging.getLogger(__name__)

# 上傳影片
async def upload_video(file: UploadFile, video: VideoCreate, user_id: int, db: Session) -> VideoOut:
    """
    上傳影片並儲存到本機
    Args:
        file: 上傳的檔案
        video: 影片創建資料
        user_id: 上傳者 ID
        db: 資料庫 Session
    Returns:
        創建的影片資料
    Raises:
        HTTPException: 如果檔案格式或大小無效
    """
    # 驗證檔案格式
    allowed_extensions = {'.mp4', '.mov', '.avi'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        logger.warning(f"Invalid file format: {file_ext}")
        raise HTTPException(status_code=400, detail="Invalid file format. Only MP4, MOV, AVI allowed.")
    
    # 驗證檔案大小（100MB）
    max_size = 100 * 1024 * 1024
    file_size = 0
    async for chunk in file:
        file_size += len(chunk)
        if file_size > max_size:
            logger.warning(f"File size too large: {file_size} bytes")
            raise HTTPException(status_code=400, detail="File size exceeds 100MB limit.")
    
    await file.seek(0)
    
    # 儲存檔案
    file_location = f"uploads/{user_id}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # 創建影片記錄
    db_video = create_video(db, video, user_id, file_location)
    return db_video

# 取得影片列表
def list_videos(db: Session) -> list[VideoOut]:
    """
    取得所有影片
    Args:
        db: 資料庫 Session
    Returns:
        影片列表
    """
    videos = get_videos(db)
    return videos

# 取得單一影片
def get_video(video_id: int, db: Session) -> VideoOut:
    """
    根據 ID 取得影片
    Args:
        video_id: 影片 ID
        db: 資料庫 Session
    Returns:
        影片資料
    Raises:
        HTTPException: 如果影片不存在
    """
    video = get_video_by_id(db, video_id)
    if not video:
        logger.warning(f"Video not found: ID {video_id}")
        raise HTTPException(status_code=404, detail="Video not found")
    return video

# 增加播放次數
def add_view_count(video_id: int, db: Session) -> dict:
    """
    增加影片播放次數
    Args:
        video_id: 影片 ID
        db: 資料庫 Session
    Returns:
        更新後的播放次數
    Raises:
        HTTPException: 如果影片不存在
    """
    view_count = increment_view_count(db, video_id)
    if view_count == 0:
        logger.warning(f"Video not found for view count: ID {video_id}")
        raise HTTPException(status_code=404, detail="Video not found")
    return {"view_count": view_count}

# 搜尋影片
def search_videos_by_query(query: str, db: Session) -> list[VideoOut]:
    """
    根據標題或上傳者搜尋影片
    Args:
        query: 搜尋關鍵字
        db: 資料庫 Session
    Returns:
        匹配的影片列表
    """
    videos = search_videos(db, query)
    return videos