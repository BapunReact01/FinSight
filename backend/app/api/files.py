from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import os
import uuid
from app.core.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.file import FileUploadResponse, FileMetadata
from app.services.azure_storage import azure_storage
from app.utils.file_handler import parse_csv, parse_excel

router = APIRouter(prefix="/files", tags=["File Storage"])

@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    company_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload CSV/Excel file to Azure Blob Storage"""
    
    # Validate file type
    allowed_extensions = ['.csv', '.xlsx', '.xls']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)
    
    # Upload to Azure Blob Storage
    file_url = None
    if azure_storage.blob_service_client:
        from io import BytesIO
        file_data = BytesIO(file_content)
        content_type = file.content_type or "application/octet-stream"
        file_url = azure_storage.upload_file(unique_filename, file_data, content_type)
    
    # Store file metadata in database (you can create a FileUpload model if needed)
    # For now, return the response
    
    return FileUploadResponse(
        file_id=0,  # Will be set when we create the FileUpload model
        file_name=file.filename,
        file_url=file_url,
        file_size=file_size,
        content_type=file.content_type or "application/octet-stream",
        uploaded_at=datetime.utcnow(),
        status="uploaded"
    )

@router.post("/parse")
async def parse_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Parse CSV/Excel file and return data"""
    
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension == '.csv':
        file_content = await file.read()
        from io import StringIO
        data = parse_csv(StringIO(file_content.decode('utf-8')))
    elif file_extension in ['.xlsx', '.xls']:
        file_content = await file.read()
        from io import BytesIO
        data = parse_excel(BytesIO(file_content))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Use CSV or Excel."
        )
    
    return {
        "file_name": file.filename,
        "rows": len(data),
        "data": data[:10]  # Return first 10 rows as preview
    }

@router.get("/list")
def list_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List uploaded files (placeholder - needs FileUpload model)"""
    return {
        "message": "File listing requires FileUpload model to be created",
        "files": []
    }