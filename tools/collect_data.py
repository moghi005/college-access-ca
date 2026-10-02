"""Copy only the raw data files the notebooks use into data/raw/.

Two Smarter Balanced files are too large for GitHub (443 MB and 466 MB).
The notebooks only use their "All Students" rows (Student Group ID == 1),
so those two files are written as subsets with only those rows. Every
other file is copied unchanged. A MANIFEST.csv with sizes and SHA-256
checksums is written to data/raw/.

Usage (local, Windows):
    python tools/collect_data.py --src "I:/Shared drives/GIS_geo_inequity/Data"

Usage (Google Colab, after mounting Drive):
    !python tools/collect_data.py --src "/content/drive/Shareddrives/GIS_geo_inequity/Data"
"""
import argparse
import csv
import hashlib
import shutil
import time
from pathlib import Path

# Files read by the notebooks (paths relative to the Data folder)
FILES = [
    "CA_school_directory/CDESchoolDirectoryExport.txt",
    "CA_school_directory/Colleges_in_California.kml",
    "NHGIS/pre_post/nhgis0039_csv/nhgis0039_ds239_20185_tract.csv",
    "NHGIS/pre_post/nhgis0039_csv/nhgis0039_ds240_20185_tract.csv",
    "NHGIS/pre_post/nhgis0039_csv/nhgis0039_ds267_20235_tract.csv",
    "NHGIS/pre_post/nhgis0039_csv/nhgis0039_ds268_20235_tract.csv",
    "NHGIS/pre_post/nhgis0039_csv/nhgis0040_ds267_20235_tract.csv",
    "SVI/SVI_Census_tracts/SVI_2014.csv",
    "SVI/SVI_Census_tracts/SVI_2016_CA.csv",
    "SVI/SVI_Census_tracts/SVI_2018_CA.csv",
    "SVI/SVI_Census_tracts/SVI_2020.csv",
    "SVI/SVI_Census_tracts/SVI_2022.csv",
    "school_related/CEnroll2021.txt",
    "school_related/StaffCred18.txt",
    "school_related/StaffDemo18.txt",
    "school_related/StaffSchoolFTE18.txt",
    "school_related/absent_2021.txt",
    "school_related/essappe2021data.xlsx",
    "school_related/free_reduced_2021.xlsx",
    "school_related/test_scores/cast_ca2021_1_csv_v2.txt",
    "school_related/test_scores/cast_ca2021entities_csv.txt",
    "school_related/test_scores/sb_ca2021entities_csv.txt",
    "school_related/16-17/cgr12mo17.txt",
    "school_related/16-17/chronicabsenteeism17.txt",
    "school_related/16-17/frpm1617.xls",
    "school_related/16-17/sb_ca2017_1_csv_v2.txt",
    "school_related/17-18/cgr12mo18.txt",
    "school_related/17-18/chronicabsenteeism18.txt",
    "school_related/17-18/frpm1718.xlsx",
    "school_related/17-18/sb_ca2018_1_csv_v3.txt",
    "school_related/18-19/cgr12mo19.txt",
    "school_related/18-19/chronicabsenteeism19.txt",
    "school_related/18-19/essappe1819data.xlsx",
    "school_related/18-19/frpm1819.xlsx",
    "school_related/18-19/sb_ca2019_1_csv_v4.txt",
    "school_related/20-21/cgr12mo21.txt",
    "school_related/20-21/chronicabsenteeism21.txt",
    "school_related/20-21/essappe2021data.xlsx",
    "school_related/20-21/frpm2021.xlsx",
    "school_related/20-21/sb_ca2021_1_csv_v2.txt",
    "school_related/21-22/cgr12mo22.txt",
    "school_related/21-22/chronicabsenteeism22-v3.txt",
    "school_related/21-22/essappe2122data.xlsx",
    "school_related/21-22/frpm2122_v2.xlsx",
    "school_related/22-23/cgr12mo23.txt",
    "school_related/22-23/chronicabsenteeism23.txt",
    "school_related/22-23/essappe2223data.xlsx",
    "school_related/22-23/frpm2223.xlsx",
]

# Folders copied whole (shapefiles and a file geodatabase)
DIRS = [
    "geographic_boundaries/ca_tracts_2022",
    "geographic_boundaries/counties",
    "geographic_boundaries/ca_counties/Ca_County_shp",
    "SVI/SVI_Census_tracts/SVI2020_CALIFORNIA_tract.gdb",
]

# Large files written as "All Students" subsets: source -> destination
SUBSETS = {
    "school_related/21-22/sb_ca2022_all_csv_v1.txt": "school_related/21-22/sb_ca2022_studentgroup1.txt",
    "school_related/22-23/sb_ca2023_all_csv_v1.txt": "school_related/22-23/sb_ca2023_studentgroup1.txt",
}


def subset_all_students(src, dst, sep="^", column="Student Group ID", keep="1"):
    """Keep the header and rows where `column` == keep. Lines are copied byte for byte."""
    kept = total = 0
    with open(src, "r", encoding="latin-1", newline="") as fin, \
         open(dst, "w", encoding="latin-1", newline="") as fout:
        header = fin.readline()
        fout.write(header)
        names = [h.strip().strip('"') for h in header.rstrip("\r\n").split(sep)]
        idx = names.index(column)
        for line in fin:
            total += 1
            fields = line.rstrip("\r\n").split(sep)
            if len(fields) > idx and fields[idx].strip().strip('"') == keep:
                fout.write(line)
                kept += 1
    return kept, total


def copy_file(src, dst, retries=6):
    """Plain read/write copy. shutil.copy2 fails on Google Drive for desktop
    (WinError 1, "Incorrect function") with Python 3.12 on Windows."""
    for attempt in range(retries):
        try:
            with open(src, "rb") as fin, open(dst, "wb") as fout:
                shutil.copyfileobj(fin, fout, 1024 * 1024)  # 1 MB reads; larger reads can fail on Drive
            break
        except OSError:
            if attempt == retries - 1:
                raise
            print(f"  retrying {src} (attempt {attempt + 2} of {retries})")
            time.sleep(10)
    try:
        shutil.copystat(src, dst)  # keep timestamps if the drive allows it
    except OSError:
        pass
    return dst


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    repo = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Original Data folder")
    ap.add_argument("--dst", default=str(repo / "data" / "raw"), help="Destination (default: data/raw)")
    args = ap.parse_args(argv)
    src, dst = Path(args.src), Path(args.dst)

    missing = [f for f in FILES + DIRS + list(SUBSETS) if not (src / f).exists()]
    if missing:
        raise SystemExit("Missing in source folder:\n  " + "\n  ".join(missing))

    for f in FILES:
        (dst / f).parent.mkdir(parents=True, exist_ok=True)
        if (dst / f).exists() and (dst / f).stat().st_size == (src / f).stat().st_size:
            print("skipped", f, "(already copied)")
            continue
        copy_file(src / f, dst / f)
        print("copied ", f)
    for d in DIRS:
        shutil.copytree(src / d, dst / d, dirs_exist_ok=True, copy_function=copy_file)
        print("copied ", d + "/")
    for s, d in SUBSETS.items():
        (dst / d).parent.mkdir(parents=True, exist_ok=True)
        kept, total = subset_all_students(src / s, dst / d)
        print(f"subset  {d}: kept {kept:,} of {total:,} rows")

    rows = []
    for p in sorted(dst.rglob("*")):
        if p.is_file() and p.name not in ("MANIFEST.csv", ".gitkeep"):
            rows.append([p.relative_to(dst).as_posix(), p.stat().st_size, sha256(p)])
    with open(dst / "MANIFEST.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "bytes", "sha256"])
        w.writerows(rows)

    total_mb = sum(r[1] for r in rows) / 1e6
    big = [r for r in rows if r[1] > 100 * 1024 * 1024]
    print(f"\n{len(rows)} files, {total_mb:,.0f} MB total. Manifest: {dst / 'MANIFEST.csv'}")
    if big:
        print("WARNING: files over GitHub's 100 MB limit:", [r[0] for r in big])


if __name__ == "__main__":
    main()
