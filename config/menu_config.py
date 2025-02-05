# search_menu/config/menu_config.py
from typing import Dict, List, Any
import json
import os
from pathlib import Path

class MenuConfig:
    """Configuration loader for menu-related settings"""
    
    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load menu configuration from JSON file"""
        config_path = Path(__file__).parent / 'menu_config.json'
        with open(config_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_valid_categories() -> List[str]:
        """Get list of valid categories"""
        config = MenuConfig.load_config()
        return config.get('valid_categories', [])

    @staticmethod
    def get_validation_rules() -> Dict[str, Any]:
        """Get validation rules"""
        config = MenuConfig.load_config()
        return config.get('validation_rules', {})