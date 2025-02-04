# manage_menus.py
import click
from datetime import datetime
import json
from typing import List, Dict
from services.menu_service import MenuService
from services.storage_service import MenuStorage
from models.menu import MenuItem
from utils.validators import validate_menu_structure

@click.group()
def cli():
    """Menu management CLI"""
    pass

@cli.command()
@click.option('--name', required=True, help='Menu name')
@click.option('--description', required=True, help='Menu description')
@click.option('--url', required=True, help='Menu URL')
@click.option('--keywords', required=True, help='Comma-separated keywords')
@click.option('--context', required=True, help='Menu context')
@click.option('--category', required=True, help='Menu category')
@click.option('--parent-id', help='Parent menu ID')
@click.option('--order', type=int, default=0, help='Menu order')
def add(name, description, url, keywords, context, category, parent_id, order):
    """Add a new menu item"""
    try:
        storage = MenuStorage()
        service = MenuService(storage)
        
        menu = MenuItem(
            name=name,
            description=description,
            url=url,
            keywords=keywords.split(','),
            context=context,
            category=category,
            parent_id=parent_id,
            order=order
        )
        
        result = service.add_menu(menu)
        click.echo(f"Added menu: {result.name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('menu_id')
@click.option('--name', help='New menu name')
@click.option('--description', help='New description')
@click.option('--url', help='New URL')
@click.option('--keywords', help='New comma-separated keywords')
@click.option('--context', help='New context')
@click.option('--category', help='New category')
@click.option('--order', type=int, help='New order')
def update(menu_id, **kwargs):
    """Update a menu item"""
    try:
        storage = MenuStorage()
        service = MenuService(storage)
        
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        if 'keywords' in update_data:
            update_data['keywords'] = update_data['keywords'].split(',')
        
        result = service.update_menu(menu_id, update_data)
        if result:
            click.echo(f"Updated menu: {result.name}")
        else:
            click.echo(f"Menu not found: {menu_id}")
    except Exception as e:
        # manage_menus.py (continued)
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def list():
    """List all menus"""
    try:
        storage = MenuStorage()
        service = MenuService(storage)
        
        menus = service.get_all_menus()
        if not menus:
            click.echo("No menus found")
            return
            
        for menu in menus:
            click.echo(f"\nID: {menu.id}")
            click.echo(f"Name: {menu.name}")
            click.echo(f"Category: {menu.category}")
            click.echo(f"URL: {menu.url}")
            click.echo(f"Active: {menu.active}")
            click.echo("---")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('menu_id')
def delete(menu_id):
    """Delete a menu item"""
    try:
        storage = MenuStorage()
        service = MenuService(storage)
        
        if service.delete_menu(menu_id):
            click.echo(f"Deleted menu: {menu_id}")
        else:
            click.echo(f"Menu not found: {menu_id}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('file_path')
def import_json(file_path):
    """Import menus from JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        storage = MenuStorage()
        service = MenuService(storage)
        
        imported = 0
        for item in data:
            if validate_menu_structure(item):
                menu = MenuItem(**item)
                service.add_menu(menu)
                imported += 1
                
        click.echo(f"Successfully imported {imported} menus")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('output_file')
def export_json(output_file):
    """Export menus to JSON file"""
    try:
        storage = MenuStorage()
        service = MenuService(storage)
        
        menus = service.get_all_menus()
        with open(output_file, 'w') as f:
            json.dump([menu.dict() for menu in menus], f, indent=2)
            
        click.echo(f"Successfully exported {len(menus)} menus to {output_file}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli()