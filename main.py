from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routers.auth_router import router as auth_router
from routers.video_router import router as video_router
from routers.comment_router import router as comment_router
import logging

# 設定日誌以便除錯
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化資料庫表
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)

# 建立 FastAPI 應用程式
app = FastAPI(title="Video Platform API", version="1.0.0")

# 掛載路由器
app.include_router(auth_router)
app.include_router(video_router)
app.include_router(comment_router)

# 提供靜態檔案（前端和上傳的影片）
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 根路徑端點
@app.get("/")
def read_root():
    return {"message": "Welcome to the Video Platform"}