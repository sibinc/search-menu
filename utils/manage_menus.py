# search_menu/scripts/manage_menus.py
import os
import sys
import click
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from search_menu.utils.menu_store import MenuStore
from search_menu.utils.logger import get_logger
from search_menu.services.menu_service import MenuService

logger = get_logger()

@click.group()
def cli():
    """Search Menu Management CLI"""
    pass

@cli.command()
@click.option('--name', prompt='Menu name')
@click.option('--description', prompt='Menu description')
@click.option('--category', prompt='Category')
@click.option('--url', prompt='URL')
def create(name, description, category, url):
    """Create a new menu interactively"""
    try:
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')  # Current time: 2025-02-05 00:21:02
        current_user = os.getenv('USER', 'sibinc')  # Current user: sibinc
        
        service = MenuService()
        
        menu_data = {
            "id": f"{category.lower()}-{int(datetime.utcnow().timestamp())}",
            "name": name,
            "description": description,
            "url": url,
            "metadata": {
                "created_at": current_time,
                "updated_at": current_time,
                "created_by": current_user,
                "updated_by": current_user,
                "version": "1.0"
            },
            "search": {
                "keywords": [],
                "synonyms": {},
                "common_phrases": {}
            },
            "category": category,
            "order": 999,
            "active": True
        }

        # Interactive keyword collection
        while True:
            keyword = click.prompt('Add a keyword (or enter to finish)', default='')
            if not keyword:
                break
            menu_data['search']['keywords'].append(keyword)

        # Interactive synonym collection
        while True:
            word = click.prompt('Add synonyms for a word (or enter to finish)', default='')
            if not word:
                break
            synonyms = click.prompt('Enter synonyms (comma-separated)').split(',')
            menu_data['search']['synonyms'][word] = [s.strip() for s in synonyms if s.strip()]

        result = service.create_menu(menu_data)
        if result:
            click.echo(f"Menu created successfully: {result.name}")
        else:
            click.echo("Failed to create menu")
    except Exception as e:
        logger.error(f"Error creating menu: {str(e)}")
        click.echo(f"Error: {str(e)}")

if __name__ == '__main__':
    cli()