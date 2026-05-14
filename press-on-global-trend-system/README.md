# press-on-global-trend-system

全球穿戴甲新品趋势监控与设计裂变系统 MVP（结构化数据版）。

## 目录结构

- `data/source_links.json` 数据源链接
- `data/sample_products.csv` 30条样本SKU
- `trend_dictionary.json` 趋势标签中英文词典
- `extract_nail_features.py` 特征提取
- `score_trends.py` 趋势打分
- `generate_design_extensions.py` 设计裂变
- `generate_packaging_extensions.py` 包装裂变
- `generate_prompts.py` Midjourney/Runway提示词
- `generate_dashboard.py` 生成可视化页面
- `main.py` 一键运行
- `output/` 输出目录

## Windows CMD 运行

```bat
cd /d D:\path\to\press-on-global-trend-system
python main.py
```

运行后打开：

- `output\press_on_global_trend_system.html`

## 输出文件

- `output/extracted_features.json`
- `output/trend_scores.json`
- `output/design_extensions.json`
- `output/packaging_extensions.json`
- `output/ai_prompts.json`
- `output/press_on_global_trend_system.html`
