import json
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "output"


def main():
    scores = json.loads((OUTPUT / "trend_scores.json").read_text(encoding="utf-8"))
    top_pack = [x["标签"] for x in scores["packaging"][:8]]
    top_style = [x["标签"] for x in scores["style"][:8]]

    items = []
    for i in range(10):
        items.append({
            "包装方案编号": f"P{i+1:03}",
            "中文主题": f"{top_style[i%len(top_style)]} x {top_pack[i%len(top_pack)]}",
            "English Packaging Name": f"Style Box {i+1}",
            "包装结构": top_pack[i%len(top_pack)],
            "文案关键词": ["giftable", "trend-driven", "global vibe"],
            "可持续建议": "优先FSC纸材与可替换内托"
        })

    (OUTPUT / "packaging_extensions.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Done: packaging extensions generated")


if __name__ == "__main__":
    main()
