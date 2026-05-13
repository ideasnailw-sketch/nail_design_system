import csv
import random
from pathlib import Path

random.seed(42)

SERIES = [
    "Nude Daily 日常裸感系列",
    "Glazed Pearl 釉光珍珠系列",
    "Clean French 干净法式系列",
    "Lavender Galaxy 薰衣草星河系列",
    "Bridal Soft White 婚礼柔白系列",
    "Jelly Summer 果冻夏日系列",
    "Cat Eye Aqua 海蓝猫眼系列",
    "Burgundy Night 酒红夜色系列",
    "Pink Party 粉色派对系列",
    "Minimal Office 极简通勤系列",
    "Chrome City 都市铬光系列",
    "Vacation Mani 度假手足系列",
]

NAIL_TYPES = ["方圆", "杏仁", "椭圆", "短方", "芭蕾"]
LENGTHS = ["短", "中", "中长"]
MAIN_COLORS = ["奶茶裸", "珍珠白", "薰衣草紫", "海盐蓝", "酒红", "樱花粉", "银铬", "豆沙粉", "奶油白", "果冻橙"]
SECONDARY_COLORS = ["香槟金", "雾灰", "亮银", "浅粉", "冰蓝", "珠光白", "玫瑰金", "透明"]
CRAFTS = ["猫眼", "渐变", "法式描边", "立体滴胶", "镜面粉", "贝壳片", "珍珠贴", "手绘花"]
ELEMENTS = ["星点", "蝴蝶结", "珍珠", "金箔", "水波纹", "碎钻", "爱心", "几何线条"]
STYLES = ["通勤", "轻奢", "甜美", "极简", "氛围感", "高级感"]
SCENES = ["日常", "约会", "婚礼", "派对", "旅行", "通勤", "拍照"]
USERS = ["学生", "白领", "新娘", "内容博主", "时尚用户"]
PACKAGING_COLORS = ["米白", "珠光白", "淡粉", "浅紫", "海盐蓝", "银灰"]
STATUSES = ["待出图", "打样中", "已确认", "可量产"]

HEADERS = [
    "款号", "系列名", "母版名", "甲型", "长度", "主色", "辅助色", "工艺", "元素", "风格", "场景", "目标用户",
    "包装主色", "英文卖点", "中文卖点", "图片路径", "打样状态", "成本", "建议售价", "设计感评分", "商业感评分",
    "生产难度评分", "包装匹配评分", "视频表现评分", "综合评分", "复盘备注"
]


def weighted_status(idx: int) -> str:
    if idx % 10 < 3:
        return "待出图"
    if idx % 10 < 6:
        return "打样中"
    if idx % 10 < 8:
        return "已确认"
    return "可量产"


def build_row(series_idx: int, sku_idx: int):
    series_name = SERIES[series_idx]
    sku_code = f"ND{series_idx + 1:02d}-{sku_idx + 1:03d}"
    master_name = f"{series_name.split()[0]} Master {sku_idx + 1:02d}"
    nail_type = random.choice(NAIL_TYPES)
    length = random.choice(LENGTHS)
    main_color = random.choice(MAIN_COLORS)
    secondary_color = random.choice(SECONDARY_COLORS)
    craft = random.choice(CRAFTS)
    element = random.choice(ELEMENTS)
    style = random.choice(STYLES)
    scene = random.choice(SCENES)
    user = random.choice(USERS)
    packaging = random.choice(PACKAGING_COLORS)

    cost = round(random.uniform(12, 36), 2)
    price = round(cost * random.uniform(2.2, 3.8), 2)
    design = round(random.uniform(6.8, 9.8), 1)
    business = round(random.uniform(6.5, 9.6), 1)
    difficulty = round(random.uniform(5.5, 9.2), 1)
    package_match = round(random.uniform(6.5, 9.7), 1)
    video_score = round(random.uniform(6.2, 9.8), 1)
    overall = round((design * 0.28 + business * 0.28 + (10 - abs(difficulty - 7.2)) * 0.12 + package_match * 0.16 + video_score * 0.16), 1)

    en_point = f"{craft} finish with {element}, {style} vibe for {scene}"
    zh_point = f"{craft}工艺结合{element}元素，呈现{style}风格，适合{scene}场景"

    image_path = f"images/raw/{sku_code}.jpg"
    status = weighted_status(sku_idx)

    return [
        sku_code, series_name, master_name, nail_type, length, main_color, secondary_color, craft, element, style, scene, user,
        packaging, en_point, zh_point, image_path, status, cost, price, design, business, difficulty,
        package_match, video_score, overall, ""
    ]


def main():
    out_path = Path("data/nail_sku_database.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for s_idx in range(12):
        for k_idx in range(10):
            rows.append(build_row(s_idx, k_idx))

    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(rows)

    print(f"已生成: {out_path}，SKU数量: {len(rows)}")


if __name__ == "__main__":
    main()
