"""Convert an original Colab notebook to the repo layout.

Removes the Google Drive mount and os.chdir lines, comments out !pip installs,
rewrites ./Data/ -> {DATA_DIR}/, ./Codes/output/ -> {OUTPUT_DIR}/,
./writing/.../figures/ -> {FIG_DIR}/, adds the path setup cell, and clears outputs.

Usage:
    python tools/clean_notebook.py 44_post_covid_neighborhood_update.ipynb notebooks/03_models/11_post_neighborhood.ipynb
"""
import json, re, sys, textwrap

SETUP = '''# Paths: edit config.py at the repo root, not this cell
import sys
from pathlib import Path
_root = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "config.py").exists())
sys.path.insert(0, str(_root))
from config import DATA_DIR, DERIVED_DIR, OUTPUT_DIR, FIG_DIR'''


def fix_paths(s):
    s = re.sub(r'''(?:\bf)?(["'])(?:\./)?Data/''', r'f\1{DATA_DIR}/', s)
    s = re.sub(r'''(?:\bf)?(["'])(?:\./)?Codes/output/''', r'f\1{OUTPUT_DIR}/', s)
    s = re.sub(r'''(?:\bf)?(["'])\./writing/[^/]+/figures/''', r'f\1{FIG_DIR}/', s)
    return s


def fix_cell(src):
    out = []
    for line in src.split('\n'):
        st = line.strip()
        if st.startswith('from google.colab import drive') or st.startswith('drive.mount('):
            continue
        if re.match(r"os\.chdir\(['\"]/content/drive", st):
            continue
        if st.startswith('!pip install'):
            line = line.replace('!pip install', '# pip install') + '  # see requirements.txt'
        line = line.replace('/content/drive/Shareddrives/GIS_geo_inequity/', './')
        out.append(fix_paths(line))
    return textwrap.dedent('\n'.join(out))


def main(src, dst):
    nb = json.load(open(src, encoding='utf-8'))
    cells = [{'cell_type': 'code', 'metadata': {}, 'source': SETUP, 'outputs': [], 'execution_count': None}]
    for c in nb['cells']:
        s = ''.join(c['source']) if isinstance(c['source'], list) else c['source']
        c['metadata'] = {}
        c.pop('id', None)
        if c['cell_type'] == 'code':
            s = fix_cell(s)
            c['outputs'] = []
            c['execution_count'] = None
        c['source'] = s
        cells.append(c)
    nb['cells'] = cells
    nb['nbformat'], nb['nbformat_minor'] = 4, 4
    nb['metadata'] = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}
    json.dump(nb, open(dst, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'wrote {dst}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
