from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

# 建立密碼雜湊上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 雜湊密碼
def hash_password(password: str) -> str:
    """
    將明文密碼雜湊
    Args:
        password: 明文密碼
    Returns:
        雜湊後的密碼
    """
    hashed = pwd_context.hash(password)
    logger.debug("Password hashed successfully")
    return hashed

# 驗證密碼
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    驗證明文密碼是否與雜湊密碼匹配
    Args:
        plain_password: 明文密碼
        hashed_password: 雜湊密碼
    Returns:
        是否匹配
    """
    verified = pwd_context.verify(plain_password, hashed_password)
    logger.debug(f"Password verification result: {verified}")
    return verified