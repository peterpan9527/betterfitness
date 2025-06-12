from fastapi import FastAPI

app = FastAPI()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import auth, videos, comments

app = FastAPI()

# 掛載路由器
app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(comments.router)

# 提供前端靜態檔案
# app.mount("/static", StaticFiles(directory="frontend"), name="static")
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Video Platform"}