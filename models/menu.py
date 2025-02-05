# models/menu.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class QueryEnhancers(BaseModel):
    primary_terms: Dict[str, str]
    action_terms: Dict[str, Dict[str, str]]
    error_tolerant_terms: Dict[str, Dict[str, List[str]]]

class SearchPhrases(BaseModel):
    questions: List[str]
    commands: List[str]
    regional_variations: Dict[str, List[str]]

class SearchMetadata(BaseModel):
    keywords: List[str]
    search_phrases: SearchPhrases
    related_terms: List[str]

class MenuDependencies(BaseModel):
    required_menus: List[str]
    optional_menus: List[str]

class WorkflowState(BaseModel):
    previous_states: List[str]
    next_states: List[str]

class MenuDetails(BaseModel):
    category: str
    subcategory: str
    context: str
    order: int
    active: bool
    permissions: List[str]
    dependencies: MenuDependencies
    workflow_state: WorkflowState

class DisplaySettings(BaseModel):
    visible: bool
    position: str

class UIComponents(BaseModel):
    icon: str
    color_scheme: Dict[str, str]
    display: Dict[str, DisplaySettings]
    notifications: Dict[str, Any]

class UsageMetrics(BaseModel):
    search_hits: int = 0
    access_count: int = 0

class MenuMetadata(BaseModel):
    created_at: datetime
    created_by: str
    updated_at: datetime
    version: str
    search_index_version: str
    last_semantic_update: datetime
    usage_metrics: UsageMetrics

class MenuItem(BaseModel):
    id: str
    name: str
    description: str
    url: str
    query_enhancers: QueryEnhancers
    search_metadata: SearchMetadata
    menu_details: MenuDetails
    ui_components: UIComponents
    metadata: MenuMetadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuItem':
        """Create MenuItem from dictionary with datetime parsing"""
        # Convert ISO datetime strings to datetime objects
        for dt_field in ['created_at', 'updated_at', 'last_semantic_update']:
            if dt_field in data.get('metadata', {}):
                data['metadata'][dt_field] = datetime.fromisoformat(
                    data['metadata'][dt_field].replace('Z', '+00:00')
                )
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper datetime formatting"""
        data = self.dict()
        # Convert datetime objects to ISO format strings
        for dt_field in ['created_at', 'updated_at', 'last_semantic_update']:
            if dt_field in data['metadata']:
                data['metadata'][dt_field] = data['metadata'][dt_field].strftime('%Y-%m-%dT%H:%M:%SZ')
        return data