# services/storage_service.py
import json
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path
import logging
from models.menu import MenuItem
from config.settings import DATA_DIR
from utils.logger import get_logger

logger = get_logger()

class StorageError(Exception):
    """Base exception for storage errors"""
    pass

class MenuStorage:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.menus_file = self.data_dir / "menus.json"
        self.enhancers_file = self.data_dir / "query_enhancers.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Ensure data directory and files exist"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            if not self.menus_file.exists():
                self.save_menus([])
            if not self.enhancers_file.exists():
                self.save_query_enhancers({})
        except Exception as e:
            logger.error(f"Failed to initialize data directory: {e}")
            raise StorageError(f"Storage initialization failed: {e}")

    def load_menus(self) -> List[MenuItem]:
        """Load menus from JSON file"""
        try:
            with open(self.menus_file, 'r') as f:
                data = json.load(f)
                return [MenuItem(**item) for item in data]
        except Exception as e:
            logger.error(f"Failed to load menus: {e}")
            raise StorageError(f"Failed to load menus: {e}")

    def save_menus(self, menus: List[MenuItem]):
        """Save menus to JSON file"""
        try:
            with open(self.menus_file, 'w') as f:
                json.dump([menu.dict() for menu in menus], f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save menus: {e}")
            raise StorageError(f"Failed to save menus: {e}")

    def load_query_enhancers(self) -> Dict[str, str]:
        """Load query enhancers from JSON file"""
        try:
            with open(self.enhancers_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load query enhancers: {e}")
            raise StorageError(f"Failed to load query enhancers: {e}")

    def save_query_enhancers(self, enhancers: Dict[str, str]):
        """Save query enhancers to JSON file"""
        try:
            with open(self.enhancers_file, 'w') as f:
                json.dump(enhancers, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save query enhancers: {e}")
            raise StorageError(f"Failed to save query enhancers: {e}")