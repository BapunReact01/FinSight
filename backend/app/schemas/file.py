from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileUploadResponse(BaseModel):
    file_id: int
    file_name: str
    file_url: Optional[str]
    file_size: int
    content_type: str
    uploaded_at: datetime
    status: str

class FileMetadata(BaseModel):
    file_name: str
    file_size: int
    content_type: str
    company_id: Optional[int] = None