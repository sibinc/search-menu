# services/storage_service.py
import json
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path
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
        self.menus_dir = self.data_dir / "menus"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.menus_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to initialize data directory: {e}")
            raise StorageError(f"Storage initialization failed: {e}")

    def load_menus(self) -> List[MenuItem]:
        """Load all menu files from the menus directory"""
        try:
            menus = []
            for file_path in self.menus_dir.glob('*.json'):
                with open(file_path, 'r') as f:
                    menu_data = json.load(f)
                    menus.append(MenuItem(**menu_data))
            return menus
        except Exception as e:
            logger.error(f"Failed to load menus: {e}")
            raise StorageError(f"Failed to load menus: {e}")

    def save_menu(self, menu: MenuItem):
        """Save a single menu to its own JSON file"""
        try:
            file_path = self.menus_dir / f"{menu.id}.json"
            with open(file_path, 'w') as f:
                json.dump(menu.dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save menu: {e}")
            raise StorageError(f"Failed to save menu: {e}")

    def delete_menu(self, menu_id: str):
        """Delete a menu file"""
        try:
            file_path = self.menus_dir / f"{menu_id}.json"
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            logger.error(f"Failed to delete menu: {e}")
            raise StorageError(f"Failed to delete menu: {e}")