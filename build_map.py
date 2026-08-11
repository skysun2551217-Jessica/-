# -*- coding: utf-8 -*-
import json, re, io, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TEMPLATE = r"C:/Users/20798/.codex/skills/trip-map-builder/assets/template.html"
OUT = r"outputs/潮汕3天2晚行程地图.html"

with io.open(TEMPLATE, encoding="utf-8") as f:
    html = f.read()

HOTEL = {"name": "桔子水晶·潮州牌坊街", "lat": 23.657916, "lng": 116.636965}

PAY = {"wechat": 1, "alipay": 1}
PAY_CASH = {"wechat": 1, "alipay": 1, "cash": 0.5}

def gmap(lat, lng):
    return f"{lat},{lng}"

DAYS = [
    {"id": 0, "label": "总览", "color": "#0071e3", "locations": []},
    {
        "id": 1, "label": "D1 潮州", "date": "8/13 周四", "title": "潮州古城 · 广济桥灯光秀", "color": "#ff9500",
        "locations": [
            {"name": "潮汕站", "lat": 23.542404, "lng": 116.582830, "type": "transport", "time": "11:45",
             "desc": "高铁抵达（约 2h）；打车到潮州古城约 30–40 分钟", "gmap": gmap(23.542404, 116.582830)},
            {"name": "桔子水晶·潮州牌坊街", "lat": 23.657916, "lng": 116.636965, "type": "hotel", "time": "12:30",
             "desc": "入住/寄存行李；城新路 35-2 号，距牌坊街约 1.5km", "pay": PAY,
             "detail": "自驾版：停车先致电酒店确认车位@@两家建议订 2–3 间房", "gmap": gmap(23.657916, 116.636965)},
            {"name": "午餐·牌坊街小吃", "lat": 23.664454, "lng": 116.645261, "type": "food", "time": "12:45",
             "desc": "肠粉、粿条、牛杂先垫肚子", "budget": "人均 ¥15–30", "pay": PAY_CASH,
             "dianpingKeyword": "潮州 肠粉", "xhsKeyword": "潮州 牌坊街 小吃", "gmap": gmap(23.664454, 116.645261)},
            {"name": "开元寺", "lat": 23.665992, "lng": 116.644691, "type": "spot", "time": "14:30",
             "desc": "唐开元二十六年建，潮州最老古刹；午后最热时段室内避暑", "budget": "免费",
             "gmap": gmap(23.665992, 116.644691)},
            {"name": "牌坊街", "lat": 23.664454, "lng": 116.645261, "type": "spot", "time": "15:30",
             "desc": "22 座明清石牌坊，边走边吃：甘草水果、杏仁茶", "budget": "免费",
             "gmap": gmap(23.664454, 116.645261)},
            {"name": "甲第巷", "lat": 23.662914, "lng": 116.643277, "type": "spot", "time": "16:30",
             "desc": "潮州民居代表，看嵌瓷门楼", "budget": "免费", "gmap": gmap(23.662914, 116.643277)},
            {"name": "广济桥", "lat": 23.665502, "lng": 116.649053, "type": "spot", "time": "17:00",
             "desc": "中国四大古桥之一；17:30 拆浮桥", "budget": "¥20", "pay": PAY,
             "detail": "20:00 广济桥灯光秀（免费，约 10 分钟）@@桥头广济楼可看夜景", "gmap": gmap(23.665502, 116.649053)},
            {"name": "晚餐·阿彬牛肉火锅（牌坊街店）", "lat": 23.663800, "lng": 116.645300, "type": "food", "time": "19:00",
             "desc": "40 年老字号，牛肉现切 12 秒起锅，沙茶+香油蘸料", "budget": "人均约 ¥100", "pay": PAY,
             "detail": "饭点排队，建议 18:45 前到或先取号", "dianpingKeyword": "阿彬牛肉火锅", "xhsKeyword": "阿彬牛肉火锅",
             "gmap": gmap(23.663800, 116.645300)},
            {"name": "胡荣泉（甜汤）", "lat": 23.664979, "lng": 116.645408, "type": "drink", "time": "20:40",
             "desc": "老字号鸭母捻、春饼、腐乳饼", "budget": "人均约 ¥15", "pay": PAY_CASH,
             "dianpingKeyword": "胡荣泉", "gmap": gmap(23.664979, 116.645408)},
        ],
    },
    {
        "id": 2, "label": "D2 汕头", "date": "8/14 周五", "title": "潮州上午 → 汕头老城 · 牛肉火锅", "color": "#ff3b30",
        "locations": [
            {"name": "韩文公祠", "lat": 23.666520, "lng": 116.655700, "type": "spot", "time": "09:00",
             "desc": "韩江东岸笔架山，纪念韩愈；周五正常开放", "budget": "免费",
             "detail": "周一闭馆（本次为周五，不受影响）", "gmap": gmap(23.666520, 116.655700)},
            {"name": "午餐·阿彬牛肉火锅（南较总店）", "lat": 23.656609, "lng": 116.637175, "type": "food", "time": "12:00",
             "desc": "潮州牛肉火锅收官；或改卤鹅+粿条", "budget": "人均约 ¥100", "pay": PAY,
             "dianpingKeyword": "阿彬牛肉火锅", "gmap": gmap(23.656609, 116.637175)},
            {"name": "转场·潮州→汕头", "lat": 23.542404, "lng": 116.582830, "type": "transport", "time": "13:30",
             "desc": "自驾约 1h 直达酒店；高铁约 20–30 分钟（经潮汕站）", "gmap": gmap(23.542404, 116.582830)},
            {"name": "全季·汕头万象城华山南路", "lat": 23.372595, "lng": 116.719742, "type": "hotel", "time": "15:00",
             "desc": "入住；华山南路 37 号鸿展大厦，近万象城/龙眼路", "pay": PAY,
             "detail": "自驾版：车停酒店，市区内打车/共享单车最省心", "gmap": gmap(23.372595, 116.719742)},
            {"name": "小公园·中山纪念亭", "lat": 23.357853, "lng": 116.669452, "type": "spot", "time": "16:00",
             "desc": "汕头老城地标，民国骑楼群", "budget": "免费", "gmap": gmap(23.357853, 116.669452)},
            {"name": "老妈宫戏台", "lat": 23.357301, "lng": 116.670863, "type": "spot", "time": "16:40",
             "desc": "潮剧老戏台，看建筑与民俗", "budget": "免费", "gmap": gmap(23.357301, 116.670863)},
            {"name": "西堤公园", "lat": 23.350168, "lng": 116.660350, "type": "spot", "time": "17:40",
             "desc": "看礐石大桥日落", "budget": "免费", "gmap": gmap(23.350168, 116.660350)},
            {"name": "广场轮渡", "lat": 23.353558, "lng": 116.680600, "type": "transport", "time": "18:10",
             "desc": "1 元渡轮跨内海湾，吹海风看日落", "budget": "¥1", "pay": PAY_CASH,
             "detail": "往返礐石，傍晚光线最好", "gmap": gmap(23.353558, 116.680600)},
            {"name": "晚餐·杏花吴记牛肉火锅", "lat": 23.367983, "lng": 116.677308, "type": "food", "time": "19:00",
             "desc": "汕头牛肉顶流、必吃榜常客；吊龙/雪花/手打牛肉丸", "budget": "人均约 ¥100", "pay": PAY,
             "detail": "早上 10 点大众点评线上取号，否则排队 2–4 小时@@备选：八合里海记（华山店，离酒店近）",
             "dianpingKeyword": "杏花吴记牛肉火锅", "xhsKeyword": "杏花吴记", "gmap": gmap(23.367983, 116.677308)},
            {"name": "龙眼南路夜宵", "lat": 23.359881, "lng": 116.706165, "type": "food", "time": "21:00",
             "desc": "回酒店顺路：小吴肠粉、蚝烙、甘草水果、糖葱薄饼", "budget": "人均 ¥30–50", "pay": PAY_CASH,
             "dianpingKeyword": "龙眼南路", "gmap": gmap(23.359881, 116.706165)},
            {"name": "开埠文化陈列馆（备选）", "lat": 23.354790, "lng": 116.669430, "type": "spot", "time": "—",
             "desc": "了解汕头开埠史（视体力加）", "budget": "免费", "gmap": gmap(23.354790, 116.669430)},
            {"name": "夜宵·生腌白粥（备选）", "lat": 23.364536, "lng": 116.699062, "type": "food", "time": "—",
             "desc": "桂园白粥 / 瑞娇嫲嫲潮汕生腌", "budget": "人均 ¥80–120", "pay": PAY,
             "detail": "生腌为生食，肠胃敏感/老人小孩建议吃熟食", "dianpingKeyword": "桂园白粥", "gmap": gmap(23.364536, 116.699062)},
        ],
    },
    {
        "id": 3, "label": "D3 返深", "date": "8/15 周六", "title": "汕头收尾 → 返程", "color": "#34c759",
        "locations": [
            {"name": "早餐·龙眼南路", "lat": 23.359881, "lng": 116.706165, "type": "food", "time": "08:00",
             "desc": "肠粉 + 亚强果汁冰/甘草水果再扫一轮", "budget": "人均 ¥20–30", "pay": PAY_CASH,
             "dianpingKeyword": "汕头 肠粉", "gmap": gmap(23.359881, 116.706165)},
            {"name": "海滨长廊·自由补漏", "lat": 23.355500, "lng": 116.683000, "type": "spot", "time": "09:30",
             "desc": "海滨长廊吹风，或补逛老城没走完的店", "budget": "免费", "gmap": gmap(23.355500, 116.683000)},
            {"name": "午餐·春梅里卤鹅", "lat": 23.359300, "lng": 116.675500, "type": "food", "time": "12:00",
             "desc": "40 年老字号，中山路 71 号；卤鹅饭/拼盘", "budget": "人均约 ¥40", "pay": PAY,
             "detail": "高铁版饭后去车站；自驾版吃完出发", "dianpingKeyword": "春梅里鹅肉", "gmap": gmap(23.359300, 116.675500)},
            {"name": "汕头站", "lat": 23.374688, "lng": 116.752430, "type": "transport", "time": "16:00",
             "desc": "高铁返程：16:33 班次 → 深圳北 18:35，20:00 前到家", "pay": PAY,
             "detail": "可选 17:14 班次（深圳北 19:39，到家约 8 点出头）@@提前订票，到站预留 30 分钟进站", "gmap": gmap(23.374688, 116.752430)},
            {"name": "自驾返程（备选）", "lat": 23.372595, "lng": 116.719742, "type": "transport", "time": "—",
             "desc": "建议 13:00–14:00 出发，约 4.5–5 小时", "detail": "午餐在汕头吃完再走，20:00 前到家", "gmap": gmap(23.372595, 116.719742)},
            {"name": "礐石风景区（备选）", "lat": 23.342500, "lng": 116.672000, "type": "spot", "time": "—",
             "desc": "广场轮渡对岸，登山看汕头湾全景（约 2–3h，午后偏热）", "budget": "门票约 ¥15", "gmap": gmap(23.342500, 116.672000)},
            {"name": "潮汕历史文化博览中心（备选）", "lat": 23.324266, "lng": 116.711077, "type": "spot", "time": "—",
             "desc": "南滨路，室内避暑，看潮汕非遗文化（约 1.5–2h）", "budget": "免费（部分临展收费）", "gmap": gmap(23.324266, 116.711077)},
            {"name": "下午茶·广场老牌豆花甜汤（备选）", "lat": 23.354777, "lng": 116.677253, "type": "drink", "time": "—",
             "desc": "老字号豆花/甜汤，老城下午茶", "budget": "人均约 ¥10", "pay": PAY_CASH, "dianpingKeyword": "广场老牌豆花甜汤", "gmap": gmap(23.354777, 116.677253)},
        ],
    },
]

OVERVIEW = """function overviewContent() {
  return `
<div class="hero"><h1>潮汕 3 天 2 晚 · 吃吃吃之旅</h1><p class="subtitle">8/13–8/15 · 潮州 + 汕头 · 两家人 5–6 人 · 吃为主线</p></div>
<div class="info-grid">
  <div class="info-card"><div class="label">酒店</div><div class="value">桔子水晶·潮州牌坊街<br>→ 全季·汕头万象城华山南路</div></div>
  <div class="info-card"><div class="label">交通</div><div class="value">高铁单程约 2h<br>自驾单程约 4.5–5h</div></div>
  <div class="info-card"><div class="label">支付</div><div class="value">微信 / 支付宝全覆盖<br>小摊备现金</div></div>
  <div class="info-card"><div class="label">预估费用</div><div class="value">人均约 ¥1,200<br>（高铁+酒店+餐饮）</div></div>
</div>
<div class="section-head">行程概览</div>
<div class="day-list">${DAYS.slice(1).map(d=>`<div class="card" onclick="go(${d.id})"><div class="name"><span class="dot" style="background:${d.color}"></span>${d.label} · ${d.title}</div><div class="desc">${d.date}</div></div>`).join('')}</div>
<div class="section-head">支付提醒</div>
<div class="info-grid">
  <div class="info-card"><div class="label">微信支付</div><div class="value">✅ 全面覆盖，主力支付</div></div>
  <div class="info-card"><div class="label">支付宝</div><div class="value">✅ 基本全覆盖</div></div>
  <div class="info-card"><div class="label">现金</div><div class="value">💴 小摊/老字号备少量</div></div>
  <div class="info-card"><div class="label">生腌提示</div><div class="value">⚠️ 生食，肠胃敏感/老人小孩建议吃熟食</div></div>
</div>
<div class="section-head">天气提示</div>
<div class="card"><div class="name">8 月高温 + 台风季</div><div class="desc">户外暴走尽量安排早晚；午后最热时段进室内/吃冰。出发前查台风预警，灯光秀雨天可能取消。</div></div>
<div class="section-head">图例</div>
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-red)"></div>餐厅</div>
  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-blue)"></div>景点</div>
  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-purple)"></div>酒吧/甜品</div>
  <div class="legend-item"><div class="legend-dot" style="background:var(--tint-orange)"></div>酒店</div>
</div>`;
}"""

html = html.replace(
    "<title><!-- REPLACE: Trip Title --></title>",
    "<title>潮汕 3 天 2 晚 · 吃吃吃之旅</title>")
html = html.replace(
    '<meta name="description" content="<!-- REPLACE: Trip Description -->">',
    '<meta name="description" content="潮州+汕头 3天2晚家庭美食之旅：牛肉火锅、生腌、卤鹅、古城与老城，交互式行程地图（2026.8.13–8.15）">')
html = html.replace(
    "const HOTEL = { name: 'Hotel Name', lat: 0, lng: 0 };",
    "const HOTEL = " + json.dumps(HOTEL, ensure_ascii=False) + ";")
days_json = json.dumps(DAYS, ensure_ascii=False).replace("@@", chr(92) + "n")
_ds = html.index("const DAYS = [")
_de = html.index("];", _ds) + 2
html = html[:_ds] + "const DAYS = " + days_json + ";" + html[_de:]
_os = html.index("function overviewContent() {")
_oe = html.index("// ╔", _os)
html = html[:_os] + OVERVIEW + chr(10) + chr(10) + html[_oe:]

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

# verify
data = io.open(OUT, encoding="utf-8").read()
m = re.search(r"const DAYS = (\[.*?\]);\n", data, re.S)
days2 = json.loads(m.group(1))
bad = [l["name"] for d in days2[1:] for l in d["locations"] if not l.get("lat") or not l.get("lng")]
bad2 = [l["name"] for d in days2[1:] for l in d["locations"] if l.get("lat") and not l.get("gmap")]
ctrl = [l["name"] for d in days2[1:] for l in d["locations"] for k in ("desc","detail") if l.get(k) and any(ord(c) < 32 for c in l[k])]
print("locations:", sum(len(d["locations"]) for d in days2[1:]))
print("missing coords:", bad if bad else "none")
print("missing gmap:", bad2 if bad2 else "none")
print("control chars in strings:", ctrl if ctrl else "none")
print("REPLACE leftover (expect 2 banner comments):", len(re.findall(r"REPLACE", data)))
print("written:", OUT, "len:", len(data))
