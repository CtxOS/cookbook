#!/usr/bin/env python3
"""Validate all cookbook recipes"""

import sys
from pathlib import Path
from ctxcook.parser import load_recipe
from ctxcook.validator import validate

def main():
    cookbooks_dir = Path('cookbooks')
    yaml_files = list(cookbooks_dir.glob('**/*.yaml')) + list(cookbooks_dir.glob('**/*.yml'))

    failed_files = []
    
    for yaml_file in yaml_files:
        try:
            recipe = load_recipe(str(yaml_file))
            validate(recipe)
            print(f'✅ {yaml_file}')
        except Exception as e:
            print(f'❌ {yaml_file}: {e}')
            failed_files.append(str(yaml_file))

    if failed_files:
        print(f'Failed validation for {len(failed_files)} files:')
        for f in failed_files:
            print(f'  - {f}')
        sys.exit(1)
    else:
        print(f'✅ All {len(yaml_files)} recipes validated successfully')

if __name__ == '__main__':
    main()
