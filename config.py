"""Project paths. Edit DATA_DIR if your raw data lives somewhere else.

Every notebook imports these three paths, so this is the only file to change.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Raw input data (see data/README.md for what goes here)
DATA_DIR = ROOT / "data" / "raw"

# Derived inputs whose original code is not in this repo (AP/IB course counts)
DERIVED_DIR = ROOT / "data" / "derived"

# Intermediate files (.pkl), model outputs, and quick-look plots
OUTPUT_DIR = ROOT / "outputs"

# Final paper figures
FIG_DIR = OUTPUT_DIR / "figures"

# Example for Google Colab with the data on a shared drive:
# DATA_DIR = Path("/content/drive/Shareddrives/GIS_geo_inequity/Data")

for _d in (OUTPUT_DIR, OUTPUT_DIR / "plots", FIG_DIR):
    _d.mkdir(parents=True, exist_ok=True)
