# School and Neighborhood Drivers of College Enrollment in California Before and During COVID-19

Code for: Liu, K. and Moghimi, A. (in review). *[Paper title]*. TODO: add journal and DOI.

The notebooks predict high school college-going rates in California from school-level and neighborhood (census tract) variables. They use XGBoost, Random Forest, Lasso, and CatBoost with Optuna tuning, explain the models with SHAP, and map spatial patterns with Gi* and bivariate Moran's I. Two periods are compared: 2016-19 (pre-COVID) and 2020-23 (during COVID).

> **Status:** all notebooks for the paper are included. Open items are in [`TODO.md`](TODO.md).

## Repository layout

```
config.py            paths used by every notebook (edit DATA_DIR here)
requirements.txt     Python packages
data/raw/            raw input data actually used (about 0.9 GB, see data/README.md)
data/derived/        AP/IB course counts per school (built by notebook 00)
notebooks/
  01_prep/           enrollment, school locations, distance to UC/CSU
  02_clean/          school and neighborhood variables for each period
  03_models/         ML models + SHAP (pre, post, pooled 2016-23)
  04_figures/        paper figures
outputs/             intermediate .pkl files and plots (created when you run)
  figures/           final paper figures
tools/               collect_data.py (builds data/raw from the original Data folder), clean_notebook.py (converts original Colab notebooks)
```

## Setup

1. Install Python 3.10+ and the packages: `pip install -r requirements.txt`
2. The raw data is included in `data/raw/` (sources and checksums in [`data/README.md`](data/README.md)).
3. Run the notebooks in numbered order. Each one lists what it reads and writes in its first cell.

**Google Colab:** clone the repo, then set `DATA_DIR` in `config.py` to your Drive path after mounting Drive.

## Notebooks and paper figures

| # | Notebook | Purpose | Main output | Paper |
|---|---|---|---|---|
| 00 | `01_prep/00_ap_ib_courses` | AP/IB course counts, 2017-18 (optional; output already in `data/derived/`) | `data/derived/school_AP_IB_courses.pkl` | Table 1 |
| 01 | `01_prep/01_enrollment_by_school` | College-going rate by school | `enrollment_by_school.pkl` | |
| 02 | `01_prep/02_school_variables_2021` | School variables and locations | `school_related.pkl` | |
| 03 | `01_prep/03_distance_to_colleges` | Distance to nearest UC and CSU | `distance_to_colleges.pkl` | |
| 04 | `02_clean/04_clean_school_2016_19` | School variables, 2016-19 | `school_related_pre.pkl` | Table 1 |
| 05 | `02_clean/05_clean_school_2020_23` | School variables, 2020-23 | `school_related_post_update.pkl` | Table 1 |
| 06 | `02_clean/06_clean_neighborhood` | Tract variables, both periods | `pre_neighborhood.pkl`, `post_neighborhood_update.pkl` | Table 1 |
| 07 | `03_models/07_pre_school` | 2016-19, school only | `24_*` | Fig 1a, 3A |
| 08 | `03_models/08_pre_neighborhood` | 2016-19, neighborhood only | `26_*` | Fig 1b, 3B |
| 09 | `03_models/09_pre_combined` | 2016-19, combined | `27_*` | Fig 1c, S1 |
| 10 | `03_models/10_post_school` | 2020-23, school only | `42_*` | Fig 1d, 3A |
| 11 | `03_models/11_post_neighborhood` | 2020-23, neighborhood only | `44_*` | Fig 1e, 3B |
| 12 | `03_models/12_post_combined` | 2020-23, combined | `45_*` | Fig 1f, S1 |
| 13 | `03_models/13_pooled_school` | 2016-23, school only | `49_*`, `plots/schoolshap.png` | Fig 2A |
| 14 | `03_models/14_pooled_neighborhood` | 2016-23, neighborhood only | `48_*`, `plots/neighborshap.png` | Fig 2B |
| 15 | `03_models/15_pooled_combined` | 2016-23, combined | `38_*` | Sec 3.1 |
| 16 | `04_figures/16_fig1_model_performance` | Ensemble performance | `figures/Figure1.tiff` | Fig 1 |
| 17 | `04_figures/17_fig3_figS1_importance_change` | Feature importance change | `figures/Figure2.tiff`, `Figure6.tiff` | Fig 3, S1 |
| 18 | `04_figures/18_fig4_key_feature_maps` | Maps of key features | `plots/keyfeatures.tiff` | Fig 4 |
| 19 | `04_figures/19_fig5_hotspots_morans` | Gi* hotspots, bivariate Moran's I | `plots/corrplot.png` | Fig 5 |

Model output files keep the numbers of the original working notebooks (for example `24_shap_values.pkl`). This lets cached Optuna studies from the original runs be reused. Each notebook header gives its original notebook name.

## Reproducibility notes

- Train/test split: spatially stratified by county, 80/20.
- Hyperparameters: Optuna (TPE sampler, fixed seed), 5-fold CV on the training set. Most models use 100 trials; some use 200 (see `TODO.md`).
- If a cached Optuna study (`outputs/<n>_<model>_trial.pkl`) exists, the notebook loads it instead of re-tuning. Delete those files to re-tune from scratch.
- Runtime: the model notebooks can take several hours each when re-tuning.

## Citation

TODO: add citation and Zenodo DOI after release.

## License

Code: MIT (see `LICENSE`). Data: see the terms of each source in `data/README.md`.
