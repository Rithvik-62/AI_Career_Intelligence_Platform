import json, os

notebooks_dir = 'notebooks'
files = sorted(os.listdir(notebooks_dir))

for fname in files:
    path = os.path.join(notebooks_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    cells = nb.get('cells', [])
    print('=' * 60)
    print('NOTEBOOK:', fname)
    print('Total cells:', len(cells))
    for i, cell in enumerate(cells[:8]):
        src = ''.join(cell.get('source', []))
        ctype = cell.get('cell_type', '')
        preview = src[:250].encode('ascii', 'ignore').decode()
        print(f'  Cell {i+1} [{ctype}]: {preview}')
    print()
