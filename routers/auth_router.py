from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from schemas import UserCreate, UserOut
from controller.auth_controller import register_user, login_user
from database import get_db
import logging

logger = logging.getLogger(__name__)

# 建立路由器
router = APIRouter(prefix="/auth", tags=["auth"])

# 註冊端點
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    註冊新使用者
    Args:
        user: 使用者創建資料
        db: 資料庫 Session
    Returns:
        創建的使用者資料
    """
    return register_user(user, db)

# 登入端點
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    使用者登入並取得 JWT token
    Args:
        username: 使用者名稱
        password: 密碼
        db: 資料庫 Session
    Returns:
        包含 access_token 的字典
    """
    return login_user(username, password, db)