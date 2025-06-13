from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Video, User
from schemas import VideoCreate
import logging

logger = logging.getLogger(__name__)

# 創建新影片
def create_video(db: Session, video: VideoCreate, user_id: int, file_path: str) -> Video:
    """
    創建新影片
    Args:
        db: 資料庫 Session
        video: 影片創建資料
        user_id: 上傳者 ID
        file_path: 檔案儲存路徑
    Returns:
        創建的 Video 物件
    """
    db_video = Video(title=video.title, file_path=file_path, user_id=user_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    logger.info(f"Created video: {video.title} by user {user_id}")
    return db_video

# 取得所有影片
def get_videos(db: Session) -> list[Video]:
    """
    取得所有影片
    Args:
        db: 資料庫 Session
    Returns:
        影片列表
    """
    videos = db.query(Video).all()
    logger.debug(f"Retrieved {len(videos)} videos")
    return videos

# 根據 ID 取得影片
def get_video_by_id(db: Session, video_id: int) -> Video:
    """
    根據影片 ID 查詢影片
    Args:
        db: 資料庫 Session
        video_id: 影片 ID
    Returns:
        Video 物件或 None
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    logger.debug(f"Queried video ID: {video_id}, found: {bool(video)}")
    return video

# 增加影片播放次數
def increment_view_count(db: Session, video_id: int) -> int:
    """
    增加影片播放次數
    Args:
        db: 資料庫 Session
        video_id: 影片 ID
    Returns:
        更新後的播放次數
    """
    video = get_video_by_id(db, video_id)
    if video:
        video.view_count += 1
        db.commit()
        logger.info(f"Incremented view count for video {video_id}: {video.view_count}")
        return video.view_count
    return 0

# 搜尋影片（根據標題或上傳者）
def search_videos(db: Session, query: str) -> list[Video]:
    """
    根據標題或上傳者搜尋影片
    Args:
        db: 資料庫 Session
        query: 搜尋關鍵字
    Returns:
        匹配的影片列表
    """
    videos = db.query(Video).join(User).filter(
        or_(
            Video.title.ilike(f"%{query}%"),
            User.username.ilike(f"%{query}%")
        )
    ).all()
    logger.debug(f"Search query '{query}' returned {len(videos)} videos")
    return videos