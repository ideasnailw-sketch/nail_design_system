import json
from itertools import islice
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "output"


def top_tags(scores, key, n=6):
    return [x["标签"] for x in islice(scores[key], n)]


def main():
    scores = json.loads((OUTPUT / "trend_scores.json").read_text(encoding="utf-8"))
    colors = top_tags(scores, "color")
    techniques = top_tags(scores, "technique")
    patterns = top_tags(scores, "pattern")
    styles = top_tags(scores, "style")

    plans = []
    for i in range(12):
        plans.append({
            "设计编号": f"D{i+1:03}",
            "中文名": f"{colors[i%len(colors)]}{patterns[i%len(patterns)]}系列",
            "English Title": f"{styles[i%len(styles)]} {techniques[i%len(techniques)]} Capsule",
            "核心元素": [colors[i%len(colors)], techniques[i%len(techniques)], patterns[i%len(patterns)]],
            "建议场景": "通勤+周末双场景",
            "价格带": "$12 - $22"
        })

    (OUTPUT / "design_extensions.json").write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Done: design extensions generated")


if __name__ == "__main__":
    main()
