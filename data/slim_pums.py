#!/usr/bin/env python3
"""Make a slim extract of the ACS 2024 1-year PUMS person file.

Usage: python3 slim_pums.py csv_pus.zip
Reads psam_pusa.csv and psam_pusb.csv straight out of the zip (no unzip needed),
keeps ages 18-66 and the variables the bridge analysis uses, and writes
acs2024_pus_slim.csv.gz next to the zip. Also prints the SHA-256 of the zip.
"""
import sys, zipfile, hashlib, gzip, csv, io, os

KEEP = ["SERIALNO", "SPORDER", "STATE", "ST", "PUMA", "AGEP", "SEX", "SCHL",
        "HICOV", "HINS1", "HINS2", "HINS3", "HINS4", "HINS5", "HINS6", "HINS7",
        "PRIVCOV", "PUBCOV", "ENG", "LANX", "ESR", "POVPIP", "RAC1P", "HISP",
        "DIS", "NATIVITY", "CIT", "PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]

def main(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    print("sha256  csv_pus.zip  " + h.hexdigest())
    out = os.path.join(os.path.dirname(os.path.abspath(path)), "acs2024_pus_slim.csv.gz")
    n_in = n_out = 0
    with zipfile.ZipFile(path) as z, gzip.open(out, "wt", newline="") as g:
        writer = None
        for name in sorted(n for n in z.namelist() if n.lower().endswith(".csv")):
            with z.open(name) as raw:
                reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", newline=""))
                cols = [c for c in KEEP if c in reader.fieldnames]
                if writer is None:
                    writer = csv.DictWriter(g, fieldnames=cols, extrasaction="ignore")
                    writer.writeheader()
                for row in reader:
                    n_in += 1
                    try:
                        age = int(row["AGEP"])
                    except (ValueError, KeyError):
                        continue
                    if 18 <= age <= 66:
                        writer.writerow(row)
                        n_out += 1
            print(f"{name}: done, rows so far {n_in:,}, kept {n_out:,}")
    print(f"wrote {out}: {n_out:,} of {n_in:,} person records")

if __name__ == "__main__":
    main(sys.argv[1])
