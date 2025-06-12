from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from schemas import VideoCreate, VideoOut
from models import Video
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import os

router = APIRouter(prefix="/videos", tags=["videos"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = "your-secret-key"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/upload", response_model=VideoOut)
async def upload_video(
    file: UploadFile = File(...),
    video: VideoCreate = Depends(),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    db_video = Video(title=video.title, file_path=file_location, user_id=user.id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video





@router.get("/", response_model=list[VideoOut])
def list_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    return videos