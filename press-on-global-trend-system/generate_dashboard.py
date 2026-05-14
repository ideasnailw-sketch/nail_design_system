import json
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "output"


def with_scores(product):
    base = len(product.get("趋势关键词", "").split(";"))
    trend = min(10, max(6, 6 + base))
    convert = 8 if "大众价" in product["价格带"] or "中价" in product["价格带"] else 7
    difficulty = 8 if any(x in product["工艺"] for x in ["3D", "猫眼", "手绘"]) else 5
    pack = 9 if any(x in product["包装风格"] for x in ["礼盒", "压纹", "烫金", "开窗"]) else 7
    video = 9 if any(x in product["风格定位"] + product["图案元素"] for x in ["Y2K", "未来", "闪", "3D", "银河", "猫眼"]) else 7
    priority = round(trend * 0.3 + convert * 0.3 + pack * 0.15 + video * 0.15 + (11 - difficulty) * 0.1, 2)
    if priority > 8:
        tag = "爆款优先开发"
    elif priority >= 7:
        tag = "重点观察"
    elif priority >= 6:
        tag = "普通裂变"
    else:
        tag = "低优先级"

    product.update({
        "趋势评分": trend,
        "商业转化评分": convert,
        "生产难度评分": difficulty,
        "包装匹配评分": pack,
        "视频表现评分": video,
        "综合开发优先级": priority,
        "优先级标签": tag,
        "可裂变方向": "色彩微调/工艺替换/场景延展",
    })
    return product


def build_sku_plans(p):
    base = p["产品"].replace(" ", "-").upper()
    variants = ["稳定复购款", "社媒吸睛款", "高级包装款"]
    plans = []
    for i, v in enumerate(variants, start=1):
        plans.append({
            "类型": v,
            "新SKU款号": f"{base}-V{i}",
            "建议系列名": f"{p['产品']} {v}",
            "设计母版名": f"{p['产品']} Master {i}",
            "甲型": p["甲型"],
            "长度": p["长度"],
            "主色": p["主色"],
            "辅助色": p["辅助色"],
            "工艺": p["工艺"],
            "图案元素": p["图案元素"],
            "使用场景": p["使用场景"],
            "目标用户": p["适合人群"],
            "包装主色": p["包装主色"],
            "包装风格": p["包装风格"],
            "英文卖点": f"{v} press-on nails with {p['工艺']} and {p['图案元素']}",
            "中文卖点": f"主打{v}，突出{p['工艺']}与{p['图案元素']}，适配{p['使用场景']}",
            "Midjourney美甲图提示词": f"press on nails, {p['主色']} and {p['辅助色']}, {p['工艺']}, {p['图案元素']}, studio shot, ultra detailed",
            "Midjourney包装图提示词": f"nail press-on packaging, {p['包装风格']}, {p['包装主色']} palette, premium retail box, 3d mockup",
            "Runway图生视频提示词": "close-up rotating press-on nails, dynamic light sweep, social media beauty ad, 4k",
        })
    return plans


def main():
    products = json.loads((OUT / "extracted_features.json").read_text(encoding="utf-8"))
    products = [with_scores(p) for p in products]
    for p in products:
        p["生成新SKU方案"] = build_sku_plans(p)

    html = """<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>全球趋势监控系统 1.1</title>
<style>body{font-family:'Microsoft YaHei',sans-serif;margin:0;background:#f5f7fb;color:#1f2937}.wrap{padding:20px}.panel{background:#fff;border-radius:12px;padding:14px;box-shadow:0 2px 10px rgba(0,0,0,.06);margin-bottom:12px}.filters{display:grid;grid-template-columns:repeat(8,minmax(120px,1fr));gap:8px}input,select,button{padding:8px;border:1px solid #d5dbe7;border-radius:8px}.btn{background:#2f54eb;color:#fff;border:none;cursor:pointer}.count{font-weight:700;color:#2f54eb}.tag{padding:4px 8px;border-radius:999px;color:#fff;font-size:12px}.爆款优先开发{background:#d7263d}.重点观察{background:#fa8c16}.普通裂变{background:#1890ff}.低优先级{background:#8c8c8c}table{width:100%;border-collapse:collapse;background:#fff}th,td{border:1px solid #eef1f7;padding:8px;font-size:12px;vertical-align:top}th{background:#f9fbff;position:sticky;top:0}.sku-card{background:#f8faff;border:1px solid #dfe7ff;border-radius:10px;padding:10px;margin:8px 0}.copy{background:#13c2c2;color:#fff;border:none;padding:4px 8px;border-radius:6px;cursor:pointer;margin-left:6px}</style></head><body><div class='wrap'>
<div class='panel'><h1>全球穿戴甲新品趋势监控与设计裂变系统 1.1</h1><p>筛选后产品总数：<span id='count' class='count'></span></p>
<div class='filters'><input id='q' placeholder='搜索品牌/产品/关键词/场景'><select id='地区'></select><select id='主色'></select><select id='工艺'></select><select id='甲型'></select><select id='包装风格'></select><select id='优先级标签'></select><button class='btn' id='reset'>重置筛选</button></div></div>
<div class='panel'><table><thead><tr><th>品牌</th><th>产品</th><th>地区</th><th>价格带</th><th>主色</th><th>辅助色</th><th>甲型</th><th>长度</th><th>工艺</th><th>图案元素</th><th>风格定位</th><th>使用场景</th><th>包装风格</th><th>包装主色</th><th>适合人群</th><th>趋势关键词</th><th>趋势评分</th><th>商业转化评分</th><th>生产难度评分</th><th>包装匹配评分</th><th>视频表现评分</th><th>综合开发优先级</th><th>可裂变方向</th><th>生成新SKU方案</th></tr></thead><tbody id='tb'></tbody></table></div></div>
<script>const data=__DATA__;const fields=['地区','主色','工艺','甲型','包装风格','优先级标签'];function fill(){fields.forEach(f=>{const s=document.getElementById(f);s.innerHTML='<option value="">全部'+f+'</option>';[...new Set(data.map(x=>x[f]))].forEach(v=>s.innerHTML+=`<option>${v}</option>`)});}
function copyText(t){navigator.clipboard.writeText(t);alert('已复制');}
function skuHtml(plans){return plans.map(p=>`<div class='sku-card'><b>${p['类型']}</b><br>新SKU款号：${p['新SKU款号']}｜建议系列名：${p['建议系列名']}｜设计母版名：${p['设计母版名']}<br>甲型/长度：${p['甲型']} / ${p['长度']}｜主辅色：${p['主色']} + ${p['辅助色']}｜工艺：${p['工艺']}｜图案元素：${p['图案元素']}<br>场景：${p['使用场景']}｜目标用户：${p['目标用户']}｜包装：${p['包装主色']} / ${p['包装风格']}<br>英文卖点：${p['英文卖点']}<br>中文卖点：${p['中文卖点']}<br>Midjourney美甲图提示词：${p['Midjourney美甲图提示词']}<button class='copy' onclick='copyText(${JSON.stringify(''+p['Midjourney美甲图提示词'])})'>一键复制</button><br>Midjourney包装图提示词：${p['Midjourney包装图提示词']}<button class='copy' onclick='copyText(${JSON.stringify(''+p['Midjourney包装图提示词'])})'>一键复制</button><br>Runway图生视频提示词：${p['Runway图生视频提示词']}<button class='copy' onclick='copyText(${JSON.stringify(''+p['Runway图生视频提示词'])})'>一键复制</button></div>`).join('')}
function render(){const q=document.getElementById('q').value.toLowerCase();let rows=data.filter(r=>{const text=[r['品牌'],r['产品'],r['趋势关键词'],r['使用场景']].join('|').toLowerCase();if(q&&!text.includes(q))return false;for(const f of fields){const v=document.getElementById(f).value;if(v&&r[f]!==v)return false;}return true;});document.getElementById('count').textContent=rows.length;const tb=document.getElementById('tb');tb.innerHTML='';rows.forEach((r,i)=>{const tr=document.createElement('tr');tr.innerHTML=`<td>${r['品牌']}</td><td>${r['产品']}</td><td>${r['地区']}</td><td>${r['价格带']}</td><td>${r['主色']}</td><td>${r['辅助色']}</td><td>${r['甲型']}</td><td>${r['长度']}</td><td>${r['工艺']}</td><td>${r['图案元素']}</td><td>${r['风格定位']}</td><td>${r['使用场景']}</td><td>${r['包装风格']}</td><td>${r['包装主色']}</td><td>${r['适合人群']}</td><td>${r['趋势关键词']}</td><td>${r['趋势评分']}</td><td>${r['商业转化评分']}</td><td>${r['生产难度评分']}</td><td>${r['包装匹配评分']}</td><td>${r['视频表现评分']}</td><td><span class='tag ${r['优先级标签']}'>${r['优先级标签']} ${r['综合开发优先级']}</span></td><td>${r['可裂变方向']}</td><td><button class='btn' onclick='toggle(${i})'>生成新 SKU 方案</button></td>`;tb.appendChild(tr);const dr=document.createElement('tr');dr.id='sku-'+i;dr.style.display='none';dr.innerHTML=`<td colspan='24'>${skuHtml(r['生成新SKU方案'])}</td>`;tb.appendChild(dr);});}
function toggle(i){const el=document.getElementById('sku-'+i);el.style.display=el.style.display==='none'?'table-row':'none';}
fill();['q',...fields].forEach(id=>document.getElementById(id).addEventListener('input',render));document.getElementById('reset').onclick=()=>{document.getElementById('q').value='';fields.forEach(f=>document.getElementById(f).value='');render();};render();</script></body></html>"""
    (OUT / "press_on_global_trend_system.html").write_text(html.replace("__DATA__", json.dumps(products, ensure_ascii=False)), encoding="utf-8")
    print("Done: dashboard generated")


if __name__ == "__main__":
    main()
