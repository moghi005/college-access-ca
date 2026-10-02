# Data

## What is in this repo

- `derived/school_AP_IB_courses.pkl` (and a `.csv` copy): number of AP and IB courses offered per school. The code that built this file was not kept. It was derived from CDE "Courses Taught" files (`CoursesTaught*.txt`) and `ClassCodes.xlsx`. Used by notebooks 02, 04, 05.

## Raw data (`raw/`)

`raw/` holds only the raw files the notebooks read (about 0.9 GB), copied from the project's original Data folder by `tools/collect_data.py`. `raw/MANIFEST.csv` lists every file with its size and SHA-256 checksum.

All files are unchanged copies of the public source files, with one exception:

- `school_related/21-22/sb_ca2022_studentgroup1.txt` and `school_related/22-23/sb_ca2023_studentgroup1.txt` are subsets of the CAASPP files `sb_ca2022_all_csv_v1.txt` (443 MB) and `sb_ca2023_all_csv_v1.txt` (466 MB). They keep the header and only the rows with `Student Group ID == 1` (All Students), copied line for line. The notebooks use only these rows, so results are identical. The originals are over GitHub's 100 MB file limit.

All sources are public. NHGIS data are used under the IPUMS terms of use; please cite IPUMS NHGIS if you reuse them.

## Rebuilding `raw/`

From the original project Data folder (only needed once, or if the data changes):

- **Colab:** open `tools/collect_data_colab.ipynb` and run all cells.
- **Local:** `python tools/collect_data.py --src "I:/Shared drives/GIS_geo_inequity/Data"`

## Layout of `raw/`

```
CA_school_directory/
  CDESchoolDirectoryExport.txt
  Colleges_in_California.kml
school_related/
  CEnroll2021.txt
  StaffCred18.txt  StaffDemo18.txt  StaffSchoolFTE18.txt
  absent_2021.txt  free_reduced_2021.xlsx  essappe2021data.xlsx
  test_scores/  sb_ca2021entities_csv.txt  cast_ca2021_1_csv_v2.txt  cast_ca2021entities_csv.txt
  16-17/  cgr12mo17.txt  chronicabsenteeism17.txt  frpm1617.xls   sb_ca2017_1_csv_v2.txt
  17-18/  cgr12mo18.txt  chronicabsenteeism18.txt  frpm1718.xlsx  sb_ca2018_1_csv_v3.txt
  18-19/  cgr12mo19.txt  chronicabsenteeism19.txt  frpm1819.xlsx  sb_ca2019_1_csv_v4.txt  essappe1819data.xlsx
  20-21/  cgr12mo21.txt  chronicabsenteeism21.txt  frpm2021.xlsx  sb_ca2021_1_csv_v2.txt  essappe2021data.xlsx
  21-22/  cgr12mo22.txt  chronicabsenteeism22-v3.txt  frpm2122_v2.xlsx  sb_ca2022_studentgroup1.txt  essappe2122data.xlsx
  22-23/  cgr12mo23.txt  chronicabsenteeism23.txt  frpm2223.xlsx  sb_ca2023_studentgroup1.txt  essappe2223data.xlsx
NHGIS/pre_post/nhgis0039_csv/
  nhgis0039_ds239_20185_tract.csv  nhgis0039_ds240_20185_tract.csv
  nhgis0039_ds267_20235_tract.csv  nhgis0039_ds268_20235_tract.csv
  nhgis0040_ds267_20235_tract.csv
SVI/SVI_Census_tracts/
  SVI_2014.csv  SVI_2016_CA.csv  SVI_2018_CA.csv  SVI_2020.csv  SVI_2022.csv
  SVI2020_CALIFORNIA_tract.gdb/
geographic_boundaries/
  ca_tracts_2022/  counties/  ca_counties/Ca_County_shp/
```

## Sources

| Data | Files | Source |
|---|---|---|
| College-going rate | `cgr12mo*.txt` | California Department of Education (CDE), DataQuest downloadable files |
| Chronic absenteeism | `chronicabsenteeism*.txt`, `absent_2021.txt` | CDE, https://www.cde.ca.gov/ds/ad/fsabd.asp |
| Free/reduced-price meals | `frpm*.xls(x)`, `free_reduced_2021.xlsx` | CDE, https://www.cde.ca.gov/ds/ad/filesspfrpm.asp |
| Per-pupil expenditure | `essappe*data.xlsx` | CDE, https://www.cde.ca.gov/fg/ac/es/essappedata.asp |
| Smarter Balanced / CAST test results | `sb_ca*.txt`, `cast_ca*.txt` (2021-22 and 2022-23: All Students subsets, see above) | CAASPP research files, https://caaspp-elpac.ets.org |
| Enrollment, staff | `CEnroll2021.txt`, `Staff*18.txt` | CDE downloadable files |
| School directory | `CDESchoolDirectoryExport.txt` | CDE, https://www.cde.ca.gov/SchoolDirectory/ |
| College locations | `Colleges_in_California.kml` | TODO: add source |
| Census tract variables | `nhgis00*.csv` | IPUMS NHGIS, https://www.nhgis.org (ACS 5-year 2014-18 and 2019-23). Check IPUMS terms before redistributing; citation required. |
| Social Vulnerability Index | `SVI_*.csv`, `.gdb` | CDC/ATSDR SVI, https://www.atsdr.cdc.gov/placeandhealth/svi/ |
| Tract and county boundaries | shapefiles | U.S. Census TIGER/Line (tracts 2022); California county boundaries |
