import json
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "output"


def main():
    features = json.loads((OUT / "extracted_features.json").read_text(encoding="utf-8"))
    scores = json.loads((OUT / "trend_scores.json").read_text(encoding="utf-8"))

    html = f"""<!doctype html>
<html lang='zh-CN'><head><meta charset='utf-8'><title>Press-on Global Trend System</title>
<style>body{{font-family:Arial;padding:20px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:8px}}th{{cursor:pointer;background:#f3f3f3}}input,select{{margin-right:8px;padding:6px}}</style>
</head><body>
<h1>全球穿戴甲新品趋势监控与设计裂变系统 MVP</h1>
<p>产品总数：{len(features)}</p>
<div><input id='q' placeholder='搜索品牌/产品'><select id='region'><option value=''>全部地区</option></select><button onclick='render()'>筛选</button></div>
<h2>产品数据</h2><table id='tbl'><thead><tr><th onclick='sortBy("brand")'>品牌</th><th onclick='sortBy("product_name")'>产品</th><th onclick='sortBy("region")'>地区</th><th onclick='sortBy("price_usd")'>价格</th><th>风格标签</th></tr></thead><tbody></tbody></table>
<h2>Top 趋势（颜色）</h2><ul>{''.join([f"<li>{x['标签']} - {x['热度分']}%</li>" for x in scores['color'][:10]])}</ul>
<script>
const data={json.dumps(features, ensure_ascii=False)};let sortKey='brand',asc=true;
const regionSel=document.getElementById('region');[...new Set(data.map(x=>x.region))].sort().forEach(r=>{{const o=document.createElement('option');o.value=r;o.textContent=r;regionSel.appendChild(o);}});
function sortBy(k){{if(sortKey===k)asc=!asc;else{{sortKey=k;asc=true;}}render();}}
function render(){{
 const q=document.getElementById('q').value.toLowerCase();const r=regionSel.value;
 let rows=data.filter(x=>(!r||x.region===r)&&((x.brand+x.product_name).toLowerCase().includes(q)));
 rows.sort((a,b)=>{{let x=a[sortKey],y=b[sortKey];if(typeof x==='number')return asc?x-y:y-x;return asc?String(x).localeCompare(String(y)):String(y).localeCompare(String(x));}});
 const tb=document.querySelector('#tbl tbody');tb.innerHTML='';
 rows.forEach(x=>{{const tr=document.createElement('tr');tr.innerHTML=`<td>${{x.brand}}</td><td>${{x.product_name}}</td><td>${{x.region}}</td><td>${{x.price_usd}}</td><td>${{x.style.map(s=>s.zh).join('、')}}</td>`;tb.appendChild(tr);}});
}}
render();
</script></body></html>"""
    (OUT / "press_on_global_trend_system.html").write_text(html, encoding="utf-8")
    print("Done: dashboard generated")


if __name__ == "__main__":
    main()
