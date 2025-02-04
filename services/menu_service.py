# services/menu_service.py
from typing import List, Optional, Dict
from datetime import datetime
import logging
from models.menu import MenuItem
from services.storage_service import MenuStorage

logger = logging.getLogger(__name__)

class MenuServiceError(Exception):
    """Base exception for menu service errors"""
    pass

class MenuService:
    def __init__(self, storage: MenuStorage):
        self.storage = storage
        self._menus: List[MenuItem] = []
        self._load_menus()

    def _load_menus(self):
        """Load menus from storage"""
        try:
            self._menus = self.storage.load_menus()
        except Exception as e:
            logger.error(f"Failed to load menus: {e}")
            raise MenuServiceError(f"Failed to load menus: {e}")

    def get_all_menus(self) -> List[MenuItem]:
        """Get all active menus"""
        return [menu for menu in self._menus if menu.active]

    def get_menu_by_id(self, menu_id: str) -> Optional[MenuItem]:
        """Get menu by ID"""
        return next((menu for menu in self._menus if menu.id == menu_id), None)

    def add_menu(self, menu: MenuItem) -> MenuItem:
        """Add a new menu item"""
        try:
            menu.created_at = datetime.utcnow()
            menu.updated_at = datetime.utcnow()
            self._menus.append(menu)
            self.storage.save_menus(self._menus)
            logger.info(f"Added new menu: {menu.name}")
            return menu
        except Exception as e:
            logger.error(f"Failed to add menu: {e}")
            raise MenuServiceError(f"Failed to add menu: {e}")

    def update_menu(self, menu_id: str, updated_data: dict) -> Optional[MenuItem]:
        """Update an existing menu item"""
        try:
            for i, menu in enumerate(self._menus):
                if menu.id == menu_id:
                    updated_data['updated_at'] = datetime.utcnow()
                    updated_menu = MenuItem(**{**menu.dict(), **updated_data})
                    self._menus[i] = updated_menu
                    self.storage.save_menus(self._menus)
                    logger.info(f"Updated menu: {menu.name}")
                    return updated_menu
            return None
        except Exception as e:
            logger.error(f"Failed to update menu: {e}")
            raise MenuServiceError(f"Failed to update menu: {e}")

    def delete_menu(self, menu_id: str) -> bool:
        """Soft delete a menu item"""
        try:
            menu = self.get_menu_by_id(menu_id)
            if menu:
                menu.active = False
                menu.updated_at = datetime.utcnow()
                self.storage.save_menus(self._menus)
                logger.info(f"Deleted menu: {menu.name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete menu: {e}")
            raise MenuServiceError(f"Failed to delete menu: {e}")

    def get_menus_by_category(self, category: str) -> List[MenuItem]:
        """Get all active menus in a category"""
        return [menu for menu in self._menus if menu.active and menu.category == category]

    def bulk_update_menus(self, updates: List[Dict]) -> List[MenuItem]:
        """Bulk update multiple menus"""
        try:
            updated_menus = []
            for update in updates:
                menu_id = update.pop('id', None)
                if menu_id:
                    updated_menu = self.update_menu(menu_id, update)
                    if updated_menu:
                        updated_menus.append(updated_menu)
            return updated_menus
        except Exception as e:
            logger.error(f"Failed to perform bulk update: {e}")
            raise MenuServiceError(f"Failed to perform bulk update: {e}")