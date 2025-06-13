from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@db:3306/video_db")
logger.info(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

# 建立資料庫引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)  # echo=False 避免過多日誌

# 建立 Session 工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立基類供模型使用
Base = declarative_base()

# 提供依賴注入的資料庫 Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")