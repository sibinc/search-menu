# search_menu/scripts/manage_menus.py
import click
import json
import os
from datetime import datetime
import time
from ..utils.menu_store import MenuStore
from ..utils.logger import get_logger
from ..models.menu import MenuItem
from ..services.menu_service import MenuService

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
        service = MenuService()
        
        menu_data = {
            "id": f"{category.lower()}-{int(time.time())}",
            "name": name,
            "description": description,
            "url": url,
            "metadata": {
                "created_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "updated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "created_by": os.getenv('USER', 'unknown'),
                "updated_by": os.getenv('USER', 'unknown'),
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