# search_menu/models/menu.py
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4
from pydantic import BaseModel, Field, validator, root_validator
import os

class MenuMetadata(BaseModel):
    """Metadata for menu items"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(default_factory=lambda: os.getenv('USER', 'sibinc'))
    updated_by: str = Field(default_factory=lambda: os.getenv('USER', 'sibinc'))
    version: str = "1.0"

class MenuSearch(BaseModel):
    """Search configuration for menu items"""
    keywords: List[str] = Field(default_factory=list)
    synonyms: Dict[str, List[str]] = Field(default_factory=dict)
    common_phrases: Dict[str, str] = Field(default_factory=dict)
    weight: float = Field(default=1.0, ge=0.0, le=2.0)

class MenuItem(BaseModel):
    """Menu item model with validation and helper methods"""
    # Core fields
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    context: str
    category: str
    order: int = Field(default=0, ge=0)
    active: bool = Field(default=True)
    parent_id: Optional[str] = None

    # Nested fields
    metadata: MenuMetadata = Field(default_factory=MenuMetadata)
    search: MenuSearch = Field(default_factory=MenuSearch)

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    @validator('url')
    def validate_url(cls, v: str) -> str:
        """Validate and format URL"""
        v = v.strip().lower()
        if not v:
            raise ValueError("URL cannot be empty")
        v = ''.join(c for c in v if c.isalnum() or c in '-_')
        return v

    @root_validator
    def validate_parent_child(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parent-child relationship"""
        parent_id = values.get('parent_id')
        item_id = values.get('id')
        
        if parent_id and parent_id == item_id:
            raise ValueError("Menu item cannot be its own parent")
        return values

    def update(self, **kwargs: Any) -> None:
        """Update menu item fields"""
        # Current timestamp: 2025-02-05 00:30:48
        # Current user: sibinc
        kwargs['metadata'] = self.metadata.dict()
        kwargs['metadata']['updated_at'] = datetime.utcnow()
        kwargs['metadata']['updated_by'] = os.getenv('USER', 'sibinc')
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper datetime formatting"""
        return {
            **self.dict(),
            'metadata': {
                **self.metadata.dict(),
                'created_at': self.metadata.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'updated_at': self.metadata.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuItem':
        """Create MenuItem from dictionary"""
        if 'metadata' not in data:
            metadata = {
                'created_at': data.pop('created_at', datetime.utcnow()),
                'updated_at': data.pop('updated_at', datetime.utcnow()),
                'created_by': data.pop('created_by', os.getenv('USER', 'sibinc')),
                'updated_by': data.pop('updated_by', os.getenv('USER', 'sibinc')),
                'version': '1.0'
            }
            data['metadata'] = metadata

        if 'search' not in data:
            data['search'] = {
                'keywords': data.pop('keywords', []),
                'synonyms': {},
                'common_phrases': {},
                'weight': 1.0
            }

        return cls(**data)

    def __str__(self) -> str:
        """String representation of the menu item"""
        return f"{self.name} ({self.id})"