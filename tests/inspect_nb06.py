import json

nb_path = 'notebooks/06_model_evaluation.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, cell in enumerate(nb['cells']):
    print(f"Cell {idx+1} ({cell.get('cell_type')}):")
    if 'source' in cell:
        src = "".join(cell['source'])
        print("  SOURCE snippet:", src[:150].replace('\n', ' '))
    if 'outputs' in cell:
        print(f"  OUTPUTS count: {len(cell['outputs'])}")
        for o_idx, out in enumerate(cell['outputs']):
            print(f"    Output {o_idx+1} type: {out.get('output_type')}")
            if 'text' in out:
                txt = "".join(out['text'])
                print("      TEXT snippet:", txt[:200].replace('\n', ' '))
