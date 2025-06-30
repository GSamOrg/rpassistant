from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import os
import uuid
from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..config import settings

router = APIRouter()

ALLOWED_EXTENSIONS = {'.pdf', '.mp3', '.wav', '.txt', '.md'}
MAX_FILE_SIZE = settings.max_file_size

async def validate_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE} bytes"
        )

@router.post("/file")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    await validate_file(file)
    
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.upload_folder) / str(current_user.id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    return {
        "filename": file.filename,
        "file_id": unique_filename,
        "file_path": str(file_path),
        "file_size": len(content)
    }

@router.get("/file/{file_id}")
async def download_file(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    file_path = Path(settings.upload_folder) / str(current_user.id) / file_id
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=file_id,
        media_type='application/octet-stream'
    )

@router.delete("/file/{file_id}")
async def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    file_path = Path(settings.upload_folder) / str(current_user.id) / file_id
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_path)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@router.get("/files")
async def list_files(current_user: User = Depends(get_current_user)):
    upload_dir = Path(settings.upload_folder) / str(current_user.id)
    
    if not upload_dir.exists():
        return {"files": []}
    
    files = []
    for file_path in upload_dir.iterdir():
        if file_path.is_file():
            files.append({
                "file_id": file_path.name,
                "file_size": file_path.stat().st_size,
                "created_at": file_path.stat().st_ctime
            })
    
    return {"files": files}