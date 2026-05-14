# press-on-global-trend-system v1.1

全球穿戴甲新品趋势监控与设计裂变系统（离线可运行）。

## v1.1 升级点

- 完整中文字段产品表（24个核心字段）。
- 自动评分：趋势评分、商业转化评分、生产难度评分、包装匹配评分、视频表现评分、综合开发优先级。
- 多维筛选：搜索、地区、主色、工艺、甲型、包装风格、优先级标签。
- 行内「生成新 SKU 方案」展开卡，内含3类方案：稳定复购款、社媒吸睛款、高级包装款。
- 每个英文提示词支持一键复制。

## 运行

```bash
cd press-on-global-trend-system
python main.py
```

打开：

- `output/press_on_global_trend_system.html`

## 输出文件

- `output/extracted_features.json`
- `output/trend_scores.json`
- `output/design_extensions.json`
- `output/packaging_extensions.json`
- `output/ai_prompts.json`
- `output/press_on_global_trend_system.html`
