# utils/menu_store.py
import os
import json
import time
from typing import Dict, List, Any
from datetime import datetime
import fcntl
from functools import lru_cache
import threading
from .logger import get_logger

logger = get_logger()

class MenuStore:
    def __init__(self):
        self.base_dir = os.path.expanduser('~/.config/search_menu')
        self.menus_dir = os.path.join(self.base_dir, 'menus')
        self.index_path = os.path.join(self.base_dir, 'menu_index.json')
        self.cache_timeout = 300  # 5 minutes
        self.last_index_check = 0
        self._index_lock = threading.Lock()
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(self.menus_dir, exist_ok=True)

    def _read_index(self) -> Dict:
        if not os.path.exists(self.index_path):
            return {'last_updated': '', 'menus': {}}

        with open(self.index_path, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                return json.load(f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def _write_index(self, index_data: Dict):
        with open(self.index_path, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                json.dump(index_data, f, indent=2)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    @lru_cache(maxsize=1)
    def get_menus(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all menus using the index"""
        try:
            self._update_index()
            index_data = self._read_index()
            
            result = []
            for menu_id, menu_info in index_data['menus'].items():
                if not active_only or menu_info['active']:
                    result.append(menu_info)
            
            return sorted(result, key=lambda x: (x['order'], x['name']))
        except Exception as e:
            logger.error(f"Error getting menus: {str(e)}")
            return []

    def search_menus(self, query: str, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Search menus with advanced scoring
        """
        try:
            self._update_index()
            index_data = self._read_index()
            query = query.lower()
            
            results = []
            for menu_id, menu_info in index_data['menus'].items():
                if not include_inactive and not menu_info['active']:
                    continue
                
                # Get full menu data for detailed search
                menu = self.get_menu(menu_id)
                if not menu:
                    continue
                
                score = self._calculate_search_score(query, menu)
                if score > 0:
                    results.append((score, menu))
            
            # Sort by score and return top matches
            results.sort(reverse=True)
            return [menu for _, menu in results[:10]]
        except Exception as e:
            logger.error(f"Error searching menus: {str(e)}")
            return []

    def _calculate_search_score(self, query: str, menu: Dict) -> float:
        """Calculate search score for a menu"""
        score = 0.0
        
        # Direct matches
        if query in menu['name'].lower():
            score += 1.0
        if query in menu['description'].lower():
            score += 0.8
            
        # Keyword matches
        keywords = menu['search']['keywords']
        if any(query in keyword.lower() for keyword in keywords):
            score += 0.8
            
        # Synonym matches
        synonyms = menu['search']['synonyms']
        for word, syns in synonyms.items():
            if query in word.lower() or any(query in syn.lower() for syn in syns):
                score += 0.6
                
        # Phrase matches
        phrases = menu['search']['common_phrases']
        for phrase in phrases:
            if query in phrase.lower():
                score += 0.7
                
        return score

    def validate_menu(self, menu_data: Dict) -> List[str]:
        """Validate menu data"""
        errors = []
        required_fields = ['id', 'name', 'description', 'url', 'category']
        
        for field in required_fields:
            if field not in menu_data:
                errors.append(f"Missing required field: {field}")
                
        if 'search' not in menu_data:
            errors.append("Missing search configuration")
        elif not isinstance(menu_data['search'], dict):
            errors.append("Invalid search configuration")
        else:
            if 'keywords' not in menu_data['search']:
                errors.append("Missing keywords in search configuration")
                
        return errors