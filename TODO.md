# Open items before the repo is made public

## Missing pieces
- [ ] **Notebook 44** (2020-23 neighborhood models). Goes in `notebooks/03_models/11_post_neighborhood.ipynb`. Its outputs (`44_*.pkl`) exist in the original `Codes/output` folder, so Fig 1 and Fig 3 can still be made. The code is missing.
- [ ] **Notebook 45** (2020-23 combined models). Goes in `notebooks/03_models/12_post_combined.ipynb`. Its outputs (`45_*.pkl`) exist in `Codes/output`. The code is missing.
  - To convert either one: `python tools/clean_notebook.py <original.ipynb> <destination.ipynb>`
- [x] **`school_AP_IB_courses.pkl`**: found in `Codes/output`. Now shipped in `data/derived/`. The code that made it is lost (`Codes/College_courses.ipynb` is related but does not produce this file: it groups by school name only and is newer than the file). Optional: recover the code.
- [ ] Source of `Colleges_in_California.kml`.

## Data
- [ ] Run `tools/collect_data.py` to fill `data/raw/` (see README). Check the printed row counts for the two Smarter Balanced subsets and that no file is over 100 MB.
- [x] The two Smarter Balanced files over 400 MB are replaced with "All Students" subsets (the only rows the code uses). Tested: same result after the notebook's filtering.
- [x] Two other missing paths were repointed to identical copies (same name and size): `cgr12mo21.txt` (now `school_related/20-21/`) and `sb_ca2021_1_csv_v2.txt` (now `school_related/20-21/`).
- [x] `nhgis0026_ds249_20205_tract.csv` (169 MB) was loaded but never used in `08`, `09`, `15`. That line is commented out.

## Decisions for the team
- [ ] **Pooled combined model (`15_pooled_combined`)**: still reads the 2020-22 files (`post_neighborhood.pkl`, `school_related_post.pkl`). Switch it to the `_update` files to match 2020-23? The paper's combined R2 = 0.62 may shift slightly.
- [ ] **Figure 4 (`18_fig4_key_feature_maps`)**: now built from the latest version, `40_map_of_key_features (1) (1).ipynb` (cividis, saves `keyfeatures.tiff`). Confirm this is the submitted figure. Caption says pre-COVID, but the code averages pre and the 2020-22 post data. Fix the caption or the code.
- [ ] **Figure 1 (`16_fig1_model_performance`)**: loads `36_pred_actual.pkl` (old pooled school model) as `all_school`. Switch it to `49_pred_actual.pkl` or remove it if it's not used in the figure.
- [ ] **Figure file names**: `17_fig3_figS1...` saves `Figure2.tiff` (paper Fig 3) and `Figure6.tiff` (paper Fig S1). Rename when numbering is final.

## Known code issues (left unchanged so results match the paper)
- [ ] Paper says 100 Optuna trials, but some models use 200: XGBoost in `08`, `14`, `15`; XGBoost, RF and Lasso in `09`; Lasso in `15`. Fix the paper text or note it.
- [ ] Cached Optuna studies are checked with a typo (`.pkl1`) for CatBoost in `13_pooled_school` and for Lasso in `10_post_school`. Those models re-tune on every run instead of loading the cached study.
- [ ] `07_pre_school` and `13_pooled_school` both write `stratified_split_train.pkl` / `stratified_split_test.pkl` (overwrite each other). These files are not read by any notebook.

## Before publishing
- [ ] Run every notebook top to bottom ("Restart and Run All") in order and confirm figures match the paper.
- [ ] Pin package versions in `requirements.txt` (`pip freeze`).
- [ ] Optional: also archive the model outputs (`Codes/output/*.pkl`) on Zenodo so figures can be remade without re-tuning.
- [ ] Connect GitHub to Zenodo, make a release, add the code DOI to the README and manuscript.
- [ ] Add a Data and Code Availability statement to the manuscript.
- [ ] Confirm license (MIT for code is the default here).
