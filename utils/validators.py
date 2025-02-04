# utils/validators.py
from typing import List, Dict
from models.menu import MenuItem

def validate_menu_structure(menu_data: Dict) -> bool:
    """Validate menu data structure"""
    required_fields = {'name', 'description', 'url', 'keywords', 'context', 'category'}
    return all(field in menu_data for field in required_fields)

def validate_menu_relationships(menus: List[MenuItem]) -> bool:
    """Validate parent-child relationships in menus"""
    menu_ids = {menu.id for menu in menus}
    for menu in menus:
        if menu.parent_id and menu.parent_id not in menu_ids:
            return False
    return True

def validate_menu_order(menus: List[MenuItem]) -> bool:
    """Validate menu order within categories"""
    category_orders = {}
    for menu in menus:
        if menu.category not in category_orders:
            category_orders[menu.category] = set()
        if menu.order in category_orders[menu.category]:
            return False
        category_orders[menu.category].add(menu.order)
    return True