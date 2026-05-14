import csv
import json
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "output"


def main():
    rows = list(csv.DictReader((DATA / "sample_products.csv").open(encoding="utf-8-sig")))
    features = []
    for idx, row in enumerate(rows, start=1):
        product = dict(row)
        product["product_id"] = f"P{idx:03d}"
        product["趋势关键词列表"] = [x.strip() for x in row.get("趋势关键词", "").split(";") if x.strip()]
        features.append(product)

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "extracted_features.json").write_text(json.dumps(features, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done: extracted {len(features)} products")


if __name__ == "__main__":
    main()
