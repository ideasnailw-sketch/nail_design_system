import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "output"


def add_counter(counter, products, field):
    for p in products:
        for token in str(p.get(field, "")).replace("/", ";").split(";"):
            token = token.strip()
            if token:
                counter[token] += 1


def format_counter(counter, total):
    return [{"标签": tag, "出现次数": cnt, "热度分": round(cnt / total * 100, 2)} for tag, cnt in counter.most_common()]


def main():
    products = json.loads((OUTPUT / "extracted_features.json").read_text(encoding="utf-8"))
    total = len(products) or 1

    c_main = Counter(); c_tech = Counter(); c_pattern = Counter(); c_style = Counter(); c_scene = Counter(); c_pack = Counter(); c_shape = Counter(); c_len = Counter()
    for field,c in [("主色",c_main),("工艺",c_tech),("图案元素",c_pattern),("风格定位",c_style),("使用场景",c_scene),("包装风格",c_pack),("甲型",c_shape),("长度",c_len)]:
        add_counter(c, products, field)

    scores = {
        "主色": format_counter(c_main,total), "工艺": format_counter(c_tech,total), "图案元素": format_counter(c_pattern,total), "风格定位": format_counter(c_style,total),
        "使用场景": format_counter(c_scene,total), "包装风格": format_counter(c_pack,total), "甲型": format_counter(c_shape,total), "长度": format_counter(c_len,total),
        "color": format_counter(c_main,total), "technique": format_counter(c_tech,total), "pattern": format_counter(c_pattern,total), "style": format_counter(c_style,total), "scene": format_counter(c_scene,total), "packaging": format_counter(c_pack,total), "shape": format_counter(c_shape,total), "length": format_counter(c_len,total)
    }

    (OUTPUT / "trend_scores.json").write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Done: trend scores generated")


if __name__ == "__main__":
    main()
