from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    coach = "coach"
    student = "student"

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole
    created_at: datetime

class VideoCreate(BaseModel):
    title: str

class VideoOut(BaseModel):
    id: int
    title: str
    file_path: str
    user_id: int
    uploaded_at: datetime

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    video_id: int
    user_id: int
    created_at: datetime