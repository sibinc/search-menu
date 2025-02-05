# services/storage_service.py
import json
from typing import List, Dict, Any
from pathlib import Path
import fcntl
from models.menu import MenuItem
from config.settings import DATA_DIR
from utils.logger import get_logger

logger = get_logger()

class StorageService:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.menus_dir = self.data_dir / "menus"
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists"""
        try:
            self.menus_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to initialize data directory: {e}")
            raise Exception(f"Storage initialization failed: {e}")

    def load_menus(self) -> List[MenuItem]:
        """Load all menu files from the menus directory"""
        menus = []
        for file_path in self.menus_dir.glob('*.json'):
            try:
                with open(file_path, 'r') as f:
                    fcntl.flock(f, fcntl.LOCK_SH)  # File lock for thread safety
                    try:
                        menu_data = json.load(f)
                        menus.append(MenuItem.from_dict(menu_data))
                    finally:
                        fcntl.flock(f, fcntl.LOCK_UN)
            except Exception as e:
                logger.error(f"Failed to load menu from {file_path}: {e}")
                continue
        return menus

    def load_menu(self, menu_id: str) -> MenuItem:
        """Load a specific menu file"""
        file_path = self.menus_dir / f"{menu_id}.json"
        try:
            with open(file_path, 'r') as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                try:
                    menu_data = json.load(f)
                    return MenuItem.from_dict(menu_data)
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except Exception as e:
            logger.error(f"Failed to load menu {menu_id}: {e}")
            raise Exception(f"Failed to load menu: {e}")