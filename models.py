from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from database import Base
import datetime
import enum
import logging

logger = logging.getLogger(__name__)

# 定義使用者角色枚舉
class UserRole(enum.Enum):
    coach = "coach"
    student = "student"

# 使用者表
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # 主鍵
    username = Column(String(50), unique=True, index=True)  # 使用者名稱，唯一
    password_hash = Column(String(255))  # 雜湊後的密碼
    role = Column(Enum(UserRole), default=UserRole.student)  # 角色（教練或學員）
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # 建立時間

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"

# 影片表
class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)  # 主鍵
    title = Column(String(100))  # 影片標題
    file_path = Column(String(255))  # 影片檔案路徑
    user_id = Column(Integer, ForeignKey("users.id"))  # 外鍵，關聯使用者
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)  # 上傳時間
    view_count = Column(Integer, default=0)  # 播放次數

    def __repr__(self):
        return f"<Video(title={self.title}, user_id={self.user_id})>"

# 留言表
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)  # 主鍵
    content = Column(Text)  # 留言內容
    video_id = Column(Integer, ForeignKey("videos.id"))  # 外鍵，關聯影片
    user_id = Column(Integer, ForeignKey("users.id"))  # 外鍵，關聯使用者
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # 留言時間

    def __repr__(self):
        return f"<Comment(video_id={self.video_id}, user_id={self.user_id})>"

logger.info("Database models defined")