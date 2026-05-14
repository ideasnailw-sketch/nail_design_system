import csv
import json
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "output"


def split_tags(raw: str):
    return [x.strip() for x in raw.split(";") if x.strip()]


def map_tags(tags, mapper):
    return [{"en": t, "zh": mapper.get(t, t)} for t in tags]


def main():
    dictionary = json.loads((BASE / "trend_dictionary.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((DATA / "sample_products.csv").open(encoding="utf-8")))
    features = []
    for row in rows:
        f = {
            "product_id": row["product_id"],
            "brand": row["brand"],
            "product_name": row["product_name"],
            "region": row["region"],
            "price_usd": float(row["price_usd"]),
            "color": map_tags(split_tags(row["color_tags"]), dictionary["color"]),
            "technique": map_tags(split_tags(row["technique_tags"]), dictionary["technique"]),
            "shape": map_tags(split_tags(row["shape_tags"]), dictionary["shape"]),
            "length": map_tags(split_tags(row["length_tags"]), dictionary["length"]),
            "pattern": map_tags(split_tags(row["pattern_tags"]), dictionary["pattern"]),
            "style": map_tags(split_tags(row["style_tags"]), dictionary["style"]),
            "scene": map_tags(split_tags(row["scene_tags"]), dictionary["scene"]),
            "packaging": map_tags(split_tags(row["packaging_tags"]), dictionary["packaging"]),
            "source": row["source"]
        }
        features.append(f)

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "extracted_features.json").write_text(json.dumps(features, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done: extracted {len(features)} products")


if __name__ == "__main__":
    main()
