# services/search_service.py
from typing import List, Tuple, Set
from models.menu import MenuItem
from services.storage_service import StorageService
from utils.logger import get_logger
from datetime import datetime

logger = get_logger()

class SearchService:
    def __init__(self):
        self.storage = StorageService()
        self._menus: List[MenuItem] = []
        self._load_menus()
        self._last_reload = datetime.utcnow()
        self.reload_interval = 300  # Reload menus every 5 minutes

    def _load_menus(self) -> None:
        """Load all menus from storage"""
        try:
            self._menus = self.storage.load_menus()
            logger.info(f"Loaded {len(self._menus)} menus")
        except Exception as e:
            logger.error(f"Failed to load menus: {e}")
            raise Exception(f"Failed to load menus: {e}")

    def _check_reload(self) -> None:
        """Check if menus need to be reloaded"""
        now = datetime.utcnow()
        if (now - self._last_reload).total_seconds() > self.reload_interval:
            self._load_menus()
            self._last_reload = now

    def _tokenize(self, text: str) -> Set[str]:
        """Convert text to lowercase tokens"""
        return set(text.lower().split())

    def search(self, query: str) -> List[Tuple[float, MenuItem]]:
        """Search menus with enhanced scoring"""
        self._check_reload()  # Ensure menus are fresh
        
        query = query.lower()
        query_tokens = self._tokenize(query)
        results = []

        for menu in self._menus:
            if not menu.menu_details.active:
                continue

            score = self._calculate_score(query, query_tokens, menu)
            if score > 0:
                results.append((score, menu))

        # Sort by score and menu order
        results.sort(key=lambda x: (-x[0], x[1].menu_details.order))
        return results

    def _calculate_score(self, query: str, query_tokens: Set[str], menu: MenuItem) -> float:
        """Calculate search score for a menu"""
        score = 0.0
        
        # Direct matches
        if query in menu.name.lower():
            score += 1.0
        if query in menu.description.lower():
            score += 0.8

        # Primary terms matching
        for term, synonyms in menu.query_enhancers.primary_terms.items():
            if term.lower() in query_tokens:
                score += 0.7
                for syn in synonyms.split():
                    if syn.lower() in query_tokens:
                        score += 0.1

        # Action terms matching
        for actions in menu.query_enhancers.action_terms.values():
            for term, synonyms in actions.items():
                if term.lower() in query_tokens:
                    score += 0.6
                    for syn in synonyms.split():
                        if syn.lower() in query_tokens:
                            score += 0.1

        # Error tolerant terms matching
        for variations in menu.query_enhancers.error_tolerant_terms.values():
            for variants in variations.values():
                if any(variant.lower() in query_tokens for variant in variants):
                    score += 0.5

        # Keywords matching
        if any(kw.lower() in query for kw in menu.search_metadata.keywords):
            score += 0.4

        # Search phrases matching
        phrases = (
            menu.search_metadata.search_phrases.questions +
            menu.search_metadata.search_phrases.commands
        )
        if any(phrase.lower() in query for phrase in phrases):
            score += 0.4

        # Regional variations matching
        for variations in menu.search_metadata.search_phrases.regional_variations.values():
            if any(var.lower() in query for var in variations):
                score += 0.3

        return score

    def get_categories(self) -> List[str]:
        """Get list of unique categories"""
        self._check_reload()
        return sorted(list(set(menu.menu_details.category for menu in self._menus)))

    def get_menus_by_category(self, category: str) -> List[MenuItem]:
        """Get all active menus in a category"""
        self._check_reload()
        return [
            menu for menu in self._menus 
            if menu.menu_details.active and menu.menu_details.category == category
        ]