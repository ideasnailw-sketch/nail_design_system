import json
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "output"


def main():
    designs = json.loads((OUTPUT / "design_extensions.json").read_text(encoding="utf-8"))
    packs = json.loads((OUTPUT / "packaging_extensions.json").read_text(encoding="utf-8"))

    prompt_rows = []
    for d, p in zip(designs[:10], packs[:10]):
        core = ", ".join(d["核心元素"])
        prompt_rows.append({
            "design_id": d["设计编号"],
            "midjourney_prompt": f"Press-on nails product shot, {d['English Title']}, {core}, studio lighting, premium e-commerce, 8k --ar 3:4",
            "runway_prompt": f"Create a 6-second beauty ad of press-on nails, focus on {d['English Title']} and {p['English Packaging Name']}, cinematic close-up, clean motion graphics"
        })

    (OUTPUT / "ai_prompts.json").write_text(json.dumps(prompt_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Done: prompts generated")


if __name__ == "__main__":
    main()
