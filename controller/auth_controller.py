from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserCreate, UserOut
from services.user_service import get_user_by_username, create_user
from secure.jwt import create_access_token
from secure.passwd import verify_password
import logging

logger = logging.getLogger(__name__)

# 註冊新使用者
def register_user(user: UserCreate, db: Session) -> UserOut:
    """
    註冊新使用者
    Args:
        user: 使用者創建資料
        db: 資料庫 Session
    Returns:
        創建的使用者資料
    Raises:
        HTTPException: 如果使用者名稱已存在
    """
    db_user = get_user_by_username(db, user.username)
    if db_user:
        logger.warning(f"Registration failed: username {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = create_user(db, user)
    return new_user

# 使用者登入
def login_user(username: str, password: str, db: Session) -> dict:
    """
    使用者登入並取得 JWT token
    Args:
        username: 使用者名稱
        password: 密碼
        db: 資料庫 Session
    Returns:
        包含 access_token 的字典
    Raises:
        HTTPException: 如果憑證無效
    """
    db_user = get_user_by_username(db, username)
    if not db_user or not verify_password(password, db_user.password_hash):
        logger.warning(f"Login failed for username: {username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    logger.info(f"User {username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}