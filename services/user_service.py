from sqlalchemy.orm import Session
from models import User
from secure.passwd import hash_password
from schemas import UserCreate
import logging

logger = logging.getLogger(__name__)

# 根據使用者名稱查詢使用者
def get_user_by_username(db: Session, username: str) -> User:
    """
    根據使用者名稱查詢使用者
    Args:
        db: 資料庫 Session
        username: 使用者名稱
    Returns:
        User 物件或 None
    """
    user = db.query(User).filter(User.username == username).first()
    logger.debug(f"Queried user: {username}, found: {bool(user)}")
    return user

# 創建新使用者
def create_user(db: Session, user: UserCreate) -> User:
    """
    創建新使用者
    Args:
        db: 資料庫 Session
        user: 使用者創建資料
    Returns:
        創建的 User 物件
    """
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, password_hash=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Created user: {user.username}")
    return db_user