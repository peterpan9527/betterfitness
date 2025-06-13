from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 認證方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 產生 JWT token
def create_access_token(data: dict) -> str:
    """
    產生 JWT token，包含過期時間
    Args:
        data: 要編碼的資料（例如 {"sub": username}）
    Returns:
        JWT token 字串
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Created JWT token for {data.get('sub')}")
    return encoded_jwt

# 驗證 JWT token 並取得使用者
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    從 JWT token 取得目前使用者
    Args:
        token: Bearer token
    Returns:
        解碼後的 payload
    Raises:
        HTTPException: 如果 token 無效或過期
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            logger.warning("Invalid JWT token: no username")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        logger.debug(f"Verified JWT token for {username}")
        return payload
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")