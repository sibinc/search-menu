# search_cli.py
import sys
from datetime import datetime
import os
from typing import List, Tuple
from models.menu import MenuItem
from services.storage_service import MenuStorage
from utils.logger import get_logger

logger = get_logger()

COLORS = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

class MenuSearchCLI:
    def __init__(self):
        self.storage = MenuStorage()
        self._menus: List[MenuItem] = []
        self._load_menus()

    def _load_menus(self):
        """Load all menus from storage"""
        try:
            self._menus = self.storage.load_menus()
            logger.info(f"Loaded {len(self._menus)} menus")
        except Exception as e:
            logger.error(f"Failed to load menus: {e}")
            raise Exception(f"Failed to load menus: {e}")

    def print_menu_result(self, score: float, menu: MenuItem):
        """Print a formatted menu search result"""
        print(f"\n{COLORS['BOLD']}{COLORS['GREEN']}Match Score: {score:.2f}{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Name:{COLORS['RESET']} {menu.name}")
        print(f"{COLORS['CYAN']}Description:{COLORS['RESET']} {menu.description}")
        print(f"{COLORS['CYAN']}Category:{COLORS['RESET']} {menu.menu_details.category}/{menu.menu_details.subcategory}")
        print(f"{COLORS['CYAN']}URL:{COLORS['RESET']} {menu.url}")
        print(f"{COLORS['CYAN']}Context:{COLORS['RESET']} {menu.menu_details.context}")
        print(f"{COLORS['YELLOW']}{'-' * 50}{COLORS['RESET']}")

    def search(self, query: str) -> List[Tuple[float, MenuItem]]:
        """Search menus with enhanced scoring"""
        query = query.lower()
        results = []

        for menu in self._menus:
            if not menu.menu_details.active:
                continue

            score = self._calculate_search_score(query, menu)
            if score > 0:
                results.append((score, menu))

        results.sort(key=lambda x: (-x[0], x[1].menu_details.order))
        return results

    def _calculate_search_score(self, query: str, menu: MenuItem) -> float:
        """Calculate search score for a menu"""
        score = 0.0
        
        # Direct matches
        if query in menu.name.lower():
            score += 1.0
        if query in menu.description.lower():
            score += 0.8

        # Primary terms matching
        for term, synonyms in menu.query_enhancers.primary_terms.items():
            if term.lower() in query or any(syn.lower() in query for syn in synonyms.split()):
                score += 0.7

        # Action terms matching
        for action_type, terms in menu.query_enhancers.action_terms.items():
            for term, synonyms in terms.items():
                if term.lower() in query or any(syn.lower() in query for syn in synonyms.split()):
                    score += 0.6

        # Error tolerant terms matching
        for error_type, variations in menu.query_enhancers.error_tolerant_terms.items():
            for term, variants in variations.items():
                if any(variant.lower() in query for variant in variants):
                    score += 0.5

        # Keywords matching
        if any(kw.lower() in query for kw in menu.search_metadata.keywords):
            score += 0.4

        # Search phrases matching
        all_phrases = (
            menu.search_metadata.search_phrases.questions +
            menu.search_metadata.search_phrases.commands
        )
        if any(phrase.lower() in query for phrase in all_phrases):
            score += 0.4

        # Regional variations matching
        for variations in menu.search_metadata.search_phrases.regional_variations.values():
            if any(var.lower() in query for var in variations):
                score += 0.3

        return score

def main():
    """Main CLI function"""
    try:
        print(f"\n{COLORS['HEADER']}Welcome to Menu Search System!{COLORS['RESET']}")
        print(f"Current Time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current User: {os.getenv('USER', 'sibinc')}\n")
        
        searcher = MenuSearchCLI()
        
        print(f"{COLORS['CYAN']}Example queries:{COLORS['RESET']}")
        print("- how to check my exam results")
        print("- where can I find my semester marks")
        print("- show regular examination results")
        print("- view my academic performance")
        print(f"\nType 'quit' to exit\n")

        while True:
            try:
                query = input(f"{COLORS['GREEN']}Enter your search query >{COLORS['RESET']} ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print(f"\n{COLORS['YELLOW']}Goodbye!{COLORS['RESET']}\n")
                    break
                
                if not query:
                    continue

                results = searcher.search(query)
                
                if not results:
                    print(f"\n{COLORS['YELLOW']}No results found. Try:{COLORS['RESET']}")
                    print("- Using different keywords")
                    print("- Being more specific")
                    print("- Checking spelling")
                    continue

                print(f"\n{COLORS['BOLD']}Found {len(results)} results:{COLORS['RESET']}")
                for score, menu in results:
                    searcher.print_menu_result(score, menu)

            except KeyboardInterrupt:
                print(f"\n{COLORS['YELLOW']}Search cancelled. Goodbye!{COLORS['RESET']}\n")
                break
            except Exception as e:
                logger.error(f"Error during search: {e}")
                print(f"\n{COLORS['RED']}An error occurred. Please try again.{COLORS['RESET']}\n")

    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        print(f"\n{COLORS['RED']}Failed to initialize search system. Please check the logs.{COLORS['RESET']}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()