# scripts/manage_menus.py
import click
import json
import os
from datetime import datetime
from utils.menu_store import MenuStore

store = MenuStore()

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
    menu = {
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
        menu['search']['keywords'].append(keyword)
    
    # Interactive synonym collection
    while True:
        word = click.prompt('Add synonyms for a word (or enter to finish)', default='')
        if not word:
            break
        synonyms = click.prompt('Enter synonyms (comma-separated)').split(',')
        menu['search']['synonyms'][word] = [s.strip() for s in synonyms if s.strip()]
    
    # Validate and save
    errors = store.validate_menu(menu)
    if errors:
        click.echo("Validation errors:")
        for error in errors:
            click.echo(f"- {error}")
        return
    
    if store.update_menu(menu):
        click.echo("Menu created successfully!")
    else:
        click.echo("Failed to create menu")

@cli.command()
@click.argument('query')
def search(query):
    """Search for menus"""
    results = store.search_menus(query)
    if not results:
        click.echo("No menus found")
        return
        
    for menu in results:
        click.echo(f"\nName: {menu['name']}")
        click.echo(f"Category: {menu['category']}")
        click.echo(f"Description: {menu['description']}")
        click.echo(f"Keywords: {', '.join(menu['search']['keywords'])}")

if __name__ == '__main__':
    cli()