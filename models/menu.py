# models/menu.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
import uuid

class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    url: str
    keywords: List[str]
    context: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True
    category: str
    order: int = 0
    parent_id: Optional[str] = None
    
    @validator('keywords')
    def keywords_not_empty(cls, v):
        if not v:
            raise ValueError('keywords list cannot be empty')
        return v

    @validator('url')
    def url_format(cls, v):
        if not v.strip():
            raise ValueError('URL cannot be empty')
        return v.lower().replace(' ', '-')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }