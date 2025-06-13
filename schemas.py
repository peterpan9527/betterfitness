from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# 使用者角色枚舉
class UserRole(str, Enum):
    coach = "coach"
    student = "student"

# 使用者創建模型（輸入）
class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

# 使用者輸出模型
class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole
    created_at: datetime

    class Config:
        orm_mode = True  # 支援從 SQLAlchemy 模型轉換

# 影片創建模型（輸入）
class VideoCreate(BaseModel):
    title: str

# 影片輸出模型
class VideoOut(BaseModel):
    id: int
    title: str
    file_path: str
    user_id: int
    uploaded_at: datetime
    view_count: int

    class Config:
        orm_mode = True

# 留言創建模型（輸入）
class CommentCreate(BaseModel):
    content: str

# 留言輸出模型
class CommentOut(BaseModel):
    id: int
    content: str
    video_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True