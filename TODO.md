# Open items before the repo is made public

## Missing pieces
- [x] **Notebooks 44 and 45** added as `11_post_neighborhood` and `12_post_combined`. Their saved R2 values (neighborhood about 0.30, combined about 0.49 per model) match the paper.
- [x] **`school_AP_IB_courses.pkl`**: rebuilt by the new `01_prep/00_ap_ib_courses` (counting method from `College_courses.ipynb`, applied to the 2017-18 Courses Taught file). Reproduces the shipped file exactly. The file itself stays in `data/derived/` because the 200 MB source is over GitHub's limit.
- [ ] Source of `Colleges_in_California.kml`.

## Data
- [x] `data/raw/` filled (118 files, about 958 MB, all sizes match the source; largest file 57 MB).
- [x] The two Smarter Balanced files over 400 MB are replaced with "All Students" subsets (the only rows the code uses). Tested: same result after the notebook's filtering.
- [x] Two other missing paths were repointed to identical copies (same name and size): `cgr12mo21.txt` (now `school_related/20-21/`) and `sb_ca2021_1_csv_v2.txt` (now `school_related/20-21/`).
- [x] `nhgis0026_ds249_20205_tract.csv` (169 MB) was loaded but never used in `08`, `09`, `15`. That line is commented out.

## Decisions for the team
- [ ] **Pooled combined model (`15_pooled_combined`)**: still reads the 2020-22 files (`post_neighborhood.pkl`, `school_related_post.pkl`). Switch it to the `_update` files to match 2020-23? The paper's combined R2 = 0.62 may shift slightly.
- [ ] **Figure 4 (`18_fig4_key_feature_maps`)**: now built from the latest version, `40_map_of_key_features (1) (1).ipynb` (cividis, saves `keyfeatures.tiff`). Confirm this is the submitted figure. Caption says pre-COVID, but the code averages pre and the 2020-22 post data. Fix the caption or the code.
- [x] **Pooled school model**: 49 is the final version (confirmed). `16_fig1_model_performance` now loads `49_pred_actual.pkl` for its extra pooled plot (not part of Fig 1).
- [ ] **Figure file names**: `17_fig3_figS1...` saves `Figure2.tiff` (paper Fig 3) and `Figure6.tiff` (paper Fig S1). Rename when numbering is final.

## Known code issues (left unchanged so results match the paper)
- [ ] Paper says 100 Optuna trials, but some models use 200: XGBoost in `08`, `14`, `15`; XGBoost, RF and Lasso in `09`; Lasso in `15`. Fix the paper text or note it.
- [ ] Cached Optuna studies are not loaded for some models, so they re-tune on every run: CatBoost in `13` and Lasso in `10` (`.pkl1` typo), Lasso and CatBoost in `11` (`.1pkl`, `t1rial`), all four models in `12` (loading commented out). With fixed seeds this should give the same studies, but it is slow.
- [ ] `07_pre_school` and `13_pooled_school` both write `stratified_split_train.pkl` / `stratified_split_test.pkl` (overwrite each other). These files are not read by any notebook.

## Before publishing
- [ ] Run every notebook top to bottom ("Restart and Run All") in order and confirm figures match the paper.
- [ ] Pin package versions in `requirements.txt` (`pip freeze`).
- [ ] Optional: also archive the model outputs (`Codes/output/*.pkl`) on Zenodo so figures can be remade without re-tuning.
- [ ] Connect GitHub to Zenodo, make a release, add the code DOI to the README and manuscript.
- [ ] Add a Data and Code Availability statement to the manuscript.
- [ ] Confirm license (MIT for code is the default here).
