import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "output"


def collect(counter, products, key):
    for p in products:
        for item in p[key]:
            counter[item["zh"]] += 1


def main():
    products = json.loads((OUTPUT / "extracted_features.json").read_text(encoding="utf-8"))
    trend_counter = {k: Counter() for k in ["color", "technique", "shape", "length", "pattern", "style", "scene", "packaging"]}

    for key, counter in trend_counter.items():
        collect(counter, products, key)

    total = len(products)
    scores = {}
    for key, counter in trend_counter.items():
        scores[key] = []
        for tag, cnt in counter.most_common():
            hot = round(cnt / total * 100, 2)
            scores[key].append({"标签": tag, "出现次数": cnt, "热度分": hot})

    (OUTPUT / "trend_scores.json").write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Done: trend scores generated")


if __name__ == "__main__":
    main()
