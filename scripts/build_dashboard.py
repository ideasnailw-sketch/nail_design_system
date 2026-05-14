import csv
import json
from pathlib import Path

DB_CSV = Path("data/nail_sku_database.csv")
PROMPT_CSV = Path("data/nail_sku_prompts.csv")
OUT_HTML = Path("outputs/dashboard.html")


def read_csv_dict(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    if not DB_CSV.exists():
        raise FileNotFoundError("请先运行 scripts/create_database.py")
    if not PROMPT_CSV.exists():
        raise FileNotFoundError("请先运行 scripts/generate_prompts.py")

    base_rows = read_csv_dict(DB_CSV)
    prompt_rows = read_csv_dict(PROMPT_CSV)
    prompt_map = {r["款号"]: r for r in prompt_rows}

    merged = []
    for r in base_rows:
        pr = prompt_map.get(r["款号"], {})
        cost = float(r["成本"])
        price = float(r["建议售价"])
        margin = ((price - cost) / price * 100) if price else 0
        r["毛利率"] = round(margin, 1)
        r["Midjourney提示词"] = pr.get("Midjourney提示词", "")
        r["包装提示词"] = pr.get("包装提示词", "")
        r["Runway视频提示词"] = pr.get("Runway视频提示词", "")
        merged.append(r)

    data_json = json.dumps(merged, ensure_ascii=False)

    html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>穿戴甲美甲设计自动化系统 2.0 总控台</title><style>
body {font-family:'Segoe UI','Microsoft YaHei',sans-serif;margin:0;background:#f4f6fb;color:#1e2430}.container{max-width:1400px;margin:0 auto;padding:20px}
.cards{display:grid;grid-template-columns:repeat(7,minmax(120px,1fr));gap:10px;margin-bottom:16px}.card{background:#fff;border-radius:12px;padding:12px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.card .label{font-size:12px;color:#667}.card .value{font-size:22px;font-weight:700;margin-top:6px}.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
input,select{padding:8px 10px;border:1px solid #ccd3df;border-radius:8px;background:#fff}table{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05)}
th,td{padding:10px 8px;border-bottom:1px solid #edf0f6;font-size:13px;text-align:left}th{background:#fafbff}tr:hover{background:#f9fbff;cursor:pointer}
.tag{padding:3px 8px;border-radius:999px;color:#fff;font-size:12px}.status-待出图{background:#8a94a8}.status-打样中{background:#f39c12}.status-已确认{background:#2e86de}.status-可量产{background:#27ae60}
.hot{color:#d63031;font-weight:700}.detail-row td{background:#fcfdff}.detail-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:8px 0}.block{background:#fff;border:1px solid #e7ebf3;border-radius:8px;padding:8px}
.block h4{margin:0 0 6px 0;font-size:13px}.block p{margin:0;font-size:12px;line-height:1.6;color:#3a4454}.btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}button{border:none;background:#304ffe;color:#fff;border-radius:8px;padding:6px 10px;cursor:pointer}
</style></head><body><div class="container"><h1>穿戴甲美甲设计自动化系统 2.0 总控台</h1>
<div class='panel-nav' style='display:grid;grid-template-columns:repeat(5,minmax(160px,1fr));gap:10px;margin-bottom:14px'>
<a class='card' href='dashboard.html'><div class='label'>SKU产品数据库系统</div><div style='font-size:12px;color:#667'>查看SKU主数据与打样进度</div></a>
<a class='card' href='#'><div class='label'>包装矩阵系统</div><div style='font-size:12px;color:#667'>包装风格组合与卖点</div></a>
<a class='card' href='#'><div class='label'>电商上架文案系统</div><div style='font-size:12px;color:#667'>标题、卖点、描述自动生成</div></a>
<a class='card' href='#'><div class='label'>短视频脚本系统</div><div style='font-size:12px;color:#667'>脚本结构与镜头建议</div></a>
<a class='card' href='../press-on-global-trend-system/output/press_on_global_trend_system.html'><div class='label'>全球趋势监控系统</div><div style='font-size:12px;color:#667'>查看全球穿戴甲新品趋势、趋势评分、包装方向、设计裂变方案。</div></a>
</div><div class="cards" id="metrics"></div>
<div class="toolbar"><input id="searchInput" placeholder="搜索款号/系列/颜色/工艺/场景" style="min-width:280px" />
<select id="seriesFilter"><option value="">全部系列</option></select><select id="statusFilter"><option value="">全部状态</option><option>待出图</option><option>打样中</option><option>已确认</option><option>可量产</option></select></div>
<table><thead><tr><th>款号</th><th>系列名</th><th>甲型</th><th>主色</th><th>工艺</th><th>场景</th><th>打样状态</th><th>成本</th><th>建议售价</th><th>毛利率</th><th>综合评分</th></tr></thead><tbody id="tableBody"></tbody></table></div>
<script>const allData=__DATA__;let openedSku=null;const toNum=v=>Number(v||0);
function calcMetrics(data){const total=data.length,series=new Set(data.map(i=>i['系列名'])).size,c=s=>data.filter(i=>i['打样状态']===s).length,avg=total?(data.reduce((a,b)=>a+toNum(b['毛利率']),0)/total).toFixed(1):'0.0';return [['SKU总数',total],['系列总数',series],['待出图数量',c('待出图')],['打样中数量',c('打样中')],['已确认数量',c('已确认')],['可量产数量',c('可量产')],['平均毛利率',avg+'%']]}
function renderMetrics(data){document.getElementById('metrics').innerHTML=calcMetrics(data).map(m=>`<div class="card"><div class="label">${m[0]}</div><div class="value">${m[1]}</div></div>`).join('')}
function buildSeriesOptions(){const sel=document.getElementById('seriesFilter');[...new Set(allData.map(i=>i['系列名']))].forEach(s=>{const op=document.createElement('option');op.value=s;op.textContent=s;sel.appendChild(op)})}
function copyText(t){navigator.clipboard.writeText(t).then(()=>alert('已复制提示词'))}
function detailHtml(r){const hot=toNum(r['综合评分'])>8?'（爆款候选）':'';return `<div class="detail-grid"><div class="block"><h4>设计标准单</h4><p>母版名：${r['母版名']}<br>甲型/长度：${r['甲型']} / ${r['长度']}<br>风格：${r['风格']}，元素：${r['元素']}${hot}</p></div><div class="block"><h4>包装标准单</h4><p>包装主色：${r['包装主色']}<br>英文卖点：${r['英文卖点']}<br>中文卖点：${r['中文卖点']}</p></div><div class="block"><h4>打样标准单</h4><p>状态：${r['打样状态']}<br>图片路径：${r['图片路径']}<br>工艺要求：${r['工艺']}</p></div><div class="block"><h4>成本标准单</h4><p>成本：¥${r['成本']}<br>建议售价：¥${r['建议售价']}<br>毛利率：${r['毛利率']}%</p></div><div class="block"><h4>质检标准单</h4><p>设计感：${r['设计感评分']}<br>生产难度：${r['生产难度评分']}<br>包装匹配：${r['包装匹配评分']}</p></div><div class="block"><h4>销售标准单</h4><p>目标用户：${r['目标用户']}<br>场景：${r['场景']}<br>综合评分：${r['综合评分']}</p></div><div class="block" style="grid-column:1/span 2;"><h4>复盘标准单</h4><p>${r['复盘备注']||'暂无复盘备注'}</p><div class="btns"><button onclick='copyText(${JSON.stringify(r['Midjourney提示词'])})'>复制 Midjourney 提示词</button><button onclick='copyText(${JSON.stringify(r['包装提示词'])})'>复制包装提示词</button><button onclick='copyText(${JSON.stringify(r['Runway视频提示词'])})'>复制 Runway 视频提示词</button></div></div></div>`}
function renderTable(data){const tb=document.getElementById('tableBody');tb.innerHTML='';data.forEach(r=>{const tr=document.createElement('tr');const hot=toNum(r['综合评分'])>8?' <span class="hot">爆款候选</span>':'';tr.innerHTML=`<td>${r['款号']}</td><td>${r['系列名']}</td><td>${r['甲型']}</td><td>${r['主色']}</td><td>${r['工艺']}</td><td>${r['场景']}</td><td><span class="tag status-${r['打样状态']}">${r['打样状态']}</span></td><td>¥${r['成本']}</td><td>¥${r['建议售价']}</td><td>${r['毛利率']}%</td><td>${r['综合评分']}${hot}</td>`;tr.onclick=()=>{openedSku=openedSku===r['款号']?null:r['款号'];applyFilters()};tb.appendChild(tr);if(openedSku===r['款号']){const dr=document.createElement('tr');dr.className='detail-row';dr.innerHTML=`<td colspan="11">${detailHtml(r)}</td>`;tb.appendChild(dr)}})}
function filteredData(){const q=document.getElementById('searchInput').value.trim().toLowerCase(),series=document.getElementById('seriesFilter').value,status=document.getElementById('statusFilter').value;return allData.filter(r=>{const pool=[r['款号'],r['系列名'],r['主色'],r['辅助色'],r['工艺'],r['场景']].join('|').toLowerCase();return (!q||pool.includes(q))&&(!series||r['系列名']===series)&&(!status||r['打样状态']===status)})}
function applyFilters(){const d=filteredData();renderMetrics(d);renderTable(d)}buildSeriesOptions();['searchInput','seriesFilter','statusFilter'].forEach(id=>document.getElementById(id).addEventListener('input',applyFilters));applyFilters();</script></body></html>"""

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html.replace("__DATA__", data_json), encoding="utf-8")
    print(f"已生成: {OUT_HTML}")


if __name__ == "__main__":
    main()
