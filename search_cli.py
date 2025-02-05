# search_cli.py
import sys
from datetime import datetime
import os
from typing import List, Tuple
from models.menu import MenuItem
from services.search_service import SearchService
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
        self.search_service = SearchService()
        self.current_time = datetime.strptime("2025-02-05 02:29:27", "%Y-%m-%d %H:%M:%S")
        self.current_user = "sibinc"

    def print_menu_result(self, score: float, menu: MenuItem):
        """Print a formatted menu search result"""
        print(f"\n{COLORS['BOLD']}{COLORS['GREEN']}Match Score: {score:.2f}{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Name:{COLORS['RESET']} {menu.name}")
        print(f"{COLORS['CYAN']}Description:{COLORS['RESET']} {menu.description}")
        print(f"{COLORS['CYAN']}Category:{COLORS['RESET']} {menu.menu_details.category}/{menu.menu_details.subcategory}")
        print(f"{COLORS['CYAN']}URL:{COLORS['RESET']} {menu.url}")
        
        # Print context if available
        if menu.menu_details.context:
            print(f"{COLORS['CYAN']}Context:{COLORS['RESET']} {menu.menu_details.context}")
        
        # Print related keywords if available
        if menu.search_metadata.keywords:
            print(f"{COLORS['CYAN']}Keywords:{COLORS['RESET']} {', '.join(menu.search_metadata.keywords)}")
        
        print(f"{COLORS['YELLOW']}{'-' * 50}{COLORS['RESET']}")

    def print_welcome_message(self):
        """Print welcome message and usage instructions"""
        print(f"\n{COLORS['HEADER']}Welcome to Menu Search System!{COLORS['RESET']}")
        print(f"Current Time (UTC): {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current User: {self.current_user}\n")
        
        print(f"{COLORS['CYAN']}Available Commands:{COLORS['RESET']}")
        print("1. search <query> - Search for menus")
        print("2. categories - List all menu categories")
        print("3. help - Show this help message")
        print("4. quit - Exit the program")
        
        print(f"\n{COLORS['CYAN']}Example queries:{COLORS['RESET']}")
        print("- how to check my exam results")
        print("- where can I find my semester marks")
        print("- show regular examination results")
        print("- view my academic performance")
        print(f"\nType 'quit' to exit\n")

    def print_categories(self):
        """Print all available menu categories"""
        categories = self.search_service.get_categories()
        if not categories:
            print(f"\n{COLORS['YELLOW']}No menu categories found.{COLORS['RESET']}\n")
            return

        print(f"\n{COLORS['BOLD']}Available Categories:{COLORS['RESET']}")
        for category in categories:
            menus = self.search_service.get_menus_by_category(category)
            active_menus = [m for m in menus if m.menu_details.active]
            print(f"\n{COLORS['CYAN']}{category}{COLORS['RESET']} ({len(active_menus)} active menus)")
            for menu in active_menus:
                print(f"  - {menu.name}")
        print()

    def print_help(self):
        """Print help information"""
        print(f"\n{COLORS['BOLD']}Menu Search Help{COLORS['RESET']}")
        print(f"\n{COLORS['CYAN']}Commands:{COLORS['RESET']}")
        print("1. search <query>  - Search for menus using natural language")
        print("2. categories     - List all available menu categories")
        print("3. help          - Show this help message")
        print("4. quit          - Exit the program")
        
        print(f"\n{COLORS['CYAN']}Search Tips:{COLORS['RESET']}")
        print("- Use natural language queries")
        print("- Include relevant keywords")
        print("- Try different phrasings")
        print("- Be specific about what you're looking for")
        
        print(f"\n{COLORS['CYAN']}Example Queries:{COLORS['RESET']}")
        print("- 'how to check exam results'")
        print("- 'where are my semester marks'")
        print("- 'show my academic performance'")
        print()

    def process_command(self, command: str) -> bool:
        """Process user command. Returns False if should exit, True otherwise."""
        command = command.strip()
        
        if not command:
            return True
            
        if command.lower() in ['quit', 'exit', 'q']:
            print(f"\n{COLORS['YELLOW']}Goodbye!{COLORS['RESET']}\n")
            return False
            
        if command.lower() == 'help':
            self.print_help()
            return True
            
        if command.lower() == 'categories':
            self.print_categories()
            return True
            
        # Treat everything else as a search query
        try:
            results = self.search_service.search(command)
            
            if not results:
                print(f"\n{COLORS['YELLOW']}No results found. Try:{COLORS['RESET']}")
                print("- Using different keywords")
                print("- Being more specific")
                print("- Checking spelling")
                print("- Type 'categories' to see available menu categories")
                print("- Type 'help' for search tips")
                return True

            print(f"\n{COLORS['BOLD']}Found {len(results)} results:{COLORS['RESET']}")
            for score, menu in results:
                self.print_menu_result(score, menu)
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            print(f"\n{COLORS['RED']}An error occurred. Please try again.{COLORS['RESET']}")
            
        return True

    def run(self):
        """Main CLI loop"""
        try:
            self.print_welcome_message()
            
            while True:
                try:
                    command = input(f"{COLORS['GREEN']}Enter search query >{COLORS['RESET']} ").strip()
                    if not self.process_command(command):
                        break
                        
                except KeyboardInterrupt:
                    print(f"\n{COLORS['YELLOW']}Search cancelled. Type 'quit' to exit.{COLORS['RESET']}")
                    continue
                    
                except EOFError:
                    print(f"\n{COLORS['YELLOW']}Input stream closed. Exiting...{COLORS['RESET']}\n")
                    break
                    
        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            print(f"\n{COLORS['RED']}An unexpected error occurred. The application will now exit.{COLORS['RESET']}\n")
            sys.exit(1)

def main():
    """Entry point for the CLI application"""
    try:
        cli = MenuSearchCLI()
        cli.run()
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        print(f"\n{COLORS['RED']}Failed to start the application. Please check the logs.{COLORS['RESET']}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()