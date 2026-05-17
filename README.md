# 穿戴甲美甲设计自动化系统 1.0（Windows 本地离线版）

本项目基于 **CSV + Python + HTML**，不依赖网络，适用于穿戴甲 SKU 的批量管理、提示词自动生成和本地可视化看板。

## 目录结构

- `data/`：CSV 数据文件
- `images/raw/`：原始图
- `images/selected/`：入选图
- `images/packaging/`：包装图
- `outputs/`：HTML 输出
- `scripts/`：自动化脚本

## 环境要求

- Windows 10/11
- Python 3.9+

## 运行命令

```bash
python scripts/create_database.py
python scripts/generate_prompts.py
python scripts/build_dashboard.py
```

## 功能说明

1. `create_database.py`
   - 生成 `data/nail_sku_database.csv`
   - 包含 12 个系列，每系列 10 个 SKU，共 120 条
   - CSV 编码为 `utf-8-sig`（Excel 打开不乱码）

2. `generate_prompts.py`
   - 根据数据库自动生成：
     - Midjourney 美甲提示词（英文）
     - 包装提示词（英文）
     - Runway 视频提示词（英文）
   - 输出到 `data/nail_sku_prompts.csv`

3. `build_dashboard.py`
   - 读取上述 CSV，生成 `outputs/dashboard.html`
   - HTML/CSS/JS 全内嵌，双击即可离线打开
   - 中文管理界面，支持搜索、筛选、状态色标签、毛利率、综合评分、爆款候选标记、行展开详情、提示词一键复制

## 使用建议

- 每次修改数据库后，按顺序重新执行三个脚本，以刷新提示词与看板。
- 打开 `outputs/dashboard.html` 即可进行本地运营管理。

## 2.0 执行版升级文档

- 详见 `docs/ecommerce_automation_execution_v2.md`，包含可直接落地的软件化分层架构、MVP 表结构、规则引擎、生命周期触发器、库存与淘汰自动化、30/60/90 天实施路线。
