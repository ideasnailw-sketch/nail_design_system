import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

STEPS = [
    "extract_nail_features.py",
    "score_trends.py",
    "generate_design_extensions.py",
    "generate_packaging_extensions.py",
    "generate_prompts.py",
    "generate_dashboard.py",
]


def run(script):
    print(f"\n>>> Running {script}")
    subprocess.run([sys.executable, str(BASE / script)], check=True)


if __name__ == "__main__":
    for step in STEPS:
        run(step)
    print("\nAll done. Open output/press_on_global_trend_system.html")
