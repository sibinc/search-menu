import sys
import os
import re
from datetime import datetime
from pathlib import Path

def camel_to_underscore(name):
    """Convert camelCase to underscore_case"""
    name = re.sub('(.)([A-Z][^A-Z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def create_menu_file(prefix):
    # Use the provided timestamp
    current_time = datetime.strptime("2025-02-05 01:10:43", "%Y-%m-%d %H:%M:%S")
    timestamp = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    
    # Get project root directory (one level up from scripts directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate filename
    prefix_underscore = camel_to_underscore(prefix)
    filename = os.path.join(data_dir, f"{prefix_underscore}_{timestamp}.json")
    
    # Create empty file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("{}\n")
    
    return filename

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_menu.py <PrefixInCamelCase>")
        print("Example: python create_menu.py RegularExaminationResults")
        sys.exit(1)
    
    prefix = sys.argv[1]
    try:
        saved_file = create_menu_file(prefix)
        print(f"Empty menu file created at: {saved_file}")
    except Exception as e:
        print(f"Error creating file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()