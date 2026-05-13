import csv
from pathlib import Path

INPUT_CSV = Path("data/nail_sku_database.csv")
OUTPUT_CSV = Path("data/nail_sku_prompts.csv")

HEADERS = [
    "款号", "Midjourney提示词", "包装提示词", "Runway视频提示词"
]


def build_prompts(row):
    sku = row["款号"]
    series = row["系列名"]
    nail_type = row["甲型"]
    length = row["长度"]
    main_color = row["主色"]
    secondary_color = row["辅助色"]
    craft = row["工艺"]
    element = row["元素"]
    style = row["风格"]
    scene = row["场景"]
    user = row["目标用户"]
    package_color = row["包装主色"]
    en_point = row["英文卖点"]

    mj = (
        f"Premium press-on nail design, SKU {sku}, collection {series}, {nail_type} shape, {length} length, "
        f"main color {main_color}, secondary color {secondary_color}, technique {craft}, detail {element}, "
        f"{style} aesthetics, for {scene}, target user {user}, studio beauty shot, soft diffused lighting, "
        f"high detail texture, clean background, product campaign quality --ar 3:4 --v 6 --stylize 250"
    )

    pkg = (
        f"Luxury wearable nail packaging design for SKU {sku}, primary package color {package_color}, "
        f"visual language from {series}, include hook line: '{en_point}', front box + inner tray + card, "
        f"minimal premium typography, cosmetic retail ready, print-ready mockup, high-end material texture"
    )

    runway = (
        f"Create a 10-second beauty commercial for press-on nails SKU {sku}. Start with macro close-up of {craft} detail, "
        f"transition to hand movement in {scene} context, highlight {main_color} and {secondary_color}, show packaging in {package_color}, "
        f"clean luxury tone, soft cinematic light, smooth camera orbit, ending with hero product frame and text: {en_point}"
    )

    return [sku, mj, pkg, runway]


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError("请先运行 scripts/create_database.py 生成基础数据库")

    with INPUT_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    out_rows = [build_prompts(r) for r in rows]

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(out_rows)

    print(f"已生成: {OUTPUT_CSV}，提示词数量: {len(out_rows)}")


if __name__ == "__main__":
    main()
