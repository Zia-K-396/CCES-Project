    if s=="charging": return '<span class="badge charge">⚡ CHARGING</span>'
    if s=="discharging": return '<span class="badge discharge">⚡ DISCHARGING</span>'
    return '<span class="badge idle">IDLE</span>'

def svg_arrow(color, direction="down"):
    return "↓" if direction=="down" else "↑"

# Build neighbourhood HTML.
nb_html=""
for i in range(5):
    stt=data["status"][i]
    frac=st.session_state.bat[i]/4
    if data["status"][i]=="discharging":
        middle=f'<div class="flowarrow blue">↑</div><div class="flowlabel blue">Li-ion → Consumers</div>'
    elif demand[i] > solar[i]:
        middle=f'<div class="flowarrow blue">↑</div><div class="flowlabel blue">CCES → Consumers</div>'
    else:
        middle=f'<div class="flowarrow orange">↑</div><div class="flowlabel orange">Excess → CCES</div>'
    if stt=="charging":
        batt=f'<div class="mini-flow"><span class="flowarrow green">↑</span><span>Solar → Li-ion</span></div>'
    elif stt=="discharging":
        batt=f'<div class="mini-flow"><span class="flowarrow blue">↓</span><span>Li-ion → Consumers</span></div>'
    else:
        batt=f'<div class="mini-flow"><span class="flowarrow gray">•</span><span>Li-ion idle</span></div>'

    support=""
    if data["transfer"][i]>.01:
        support='<div class="support">← OTHER NB Li-ion SUPPORT</div>'
    elif data["transfer"][i]<-.01:
        support='<div class="support">OTHER NB Li-ion →</div>'

    nb_html+=f"""
    <div class="nbcard">
      <div class="nbhead nb{i}">
        <span class="house">⌂</span>
        <span><b>Neighbourhood {i+1}</b><br><small>4,000 consumers</small></span>
      </div>
      <div class="nbbody">
        <div class="row"><span>☀️ Rooftop Solar Generation</span><b>{solar[i]:.1f} MW</b></div>
        <div class="row"><span>▥ Current Demand</span><b>{demand[i]:.1f} MW</b></div>
        <div class="row"><span>🔋 Li-ion Battery</span><b>{st.session_state.bat[i]:.1f} / 4 MWh ({frac*100:.0f}%)</b></div>
        <div class="bar"><i style="width:{frac*100:.1f}%"></i></div>
        {battery_badge(i)}
        <div class="pf">Power Flow (Current)</div>
        <div class="flowgrid">
          <div><div class="flowarrow green">↓</div><b>{solar[i]:.1f} MW</b><small>from Solar</small></div>
          <div><div class="flowarrow {'blue' if demand[i]>solar[i] else 'orange'}">
             {'↑' if demand[i]>solar[i] else '↓'}</div>
             <b>{abs(demand[i]-solar[i]):.1f} MW</b>
             <small>{'from CCES' if demand[i]>solar[i] else 'to CCES'}</small></div>
          <div><div class="flowarrow {'blue' if stt=='discharging' else 'green'}">
             {'↓' if stt=='discharging' else '↑' if stt=='charging' else '•'}</div>
             <b>{'ACTIVE' if stt!='idle' else '—'}</b>
             <small>{'Li-ion' if stt!='idle' else 'idle'}</small></div>
        </div>
        {support}
      </div>
    </div>
    """

# Simple SVG line chart builder.
def chart_svg(title, values, color, ymax, unit):
    if not values:
        values=[0,0]
    vals=values[-96:]
    w,h=360,120
    left,top=30,20
    pw,ph=320,78
    pts=[]
    for j,v in enumerate(vals):
        x=left+(j/max(1,len(vals)-1))*pw
        y=top+ph-(max(0,min(ymax,v))/ymax)*ph
        pts.append(f"{x:.1f},{y:.1f}")
    poly=" ".join(pts)
    return f"""
    <div class="chartbox">
      <div class="charttitle">{title}</div>
      <svg viewBox="0 0 {w} {h}" width="100%" height="120">
        <line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" stroke="#dbe4ee"/>
        <line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#dbe4ee"/>
        <polyline points="{poly}" fill="none" stroke="{color}" stroke-width="3"/>
        <text x="{left}" y="116" font-size="9" fill="#64748b">12 AM</text>
        <text x="{left+pw/2}" y="116" font-size="9" fill="#64748b" text-anchor="middle">12 PM</text>
        <text x="{left+pw}" y="116" font-size="9" fill="#64748b" text-anchor="end">12 AM</text>
      </svg>
    </div>
    """

hist=st.session_state.hist
if not hist["solar"]:
    # Reference curves until simulation has produced history.
    hours=[i/4 for i in range(97)]
    hist_s=[30*max(0,math.sin(math.pi*(h-5.5)/13)) if 5.5<=h<=18.5 else 0 for h in hours]
    hist_d=[8+7*max(0,math.sin(math.pi*(h-7)/14))+4*(1 if h>=18 else 0) for h in hours]
    hist_c=[60-32*max(0,math.sin(math.pi*(h-6)/12)) if 6<=h<=18 else 60 for h in hours]
    hist_l=[8+6*max(0,math.sin(math.pi*(h-6)/12)) if 6<=h<=18 else 8 for h in hours]
else:
    hist_s=hist["solar"];hist_d=hist["demand"];hist_c=hist["cces"];hist_l=hist["liion"]

html=f"""
<style>
.dashboard{{font-family:Arial,Helvetica,sans-serif;color:#10243e;background:#f4f7fb}}
.panel{{background:#fff;border:1px solid #b9c7d8;border-radius:11px;padding:9px 11px;box-sizing:border-box}}
.gridtop{{display:grid;grid-template-columns:1.7fr 2.0fr 1.25fr;gap:8px}}
.main{{display:grid;grid-template-columns:1.0fr 3.35fr 1.18fr;gap:7px;margin-top:6px}}
.nbs{{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:6px}}
.charts{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}}
.title{{font-size:18px;font-weight:800;margin-bottom:10px}}
.sub{{font-size:11px;color:#64748b}}
.kv{{display:flex;justify-content:space-between;font-size:11px;margin:9px 0}}
.bar{{height:10px;background:#e6edf5;border-radius:6px;overflow:hidden;margin:5px 0 8px}}
.bar i{{display:block;height:100%;background:#16a34a;border-radius:6px}}
.orangebar i{{background:#f59e0b}}
.bluebar i{{background:#1677e8}}
.solarbox,.flowbox{{border:1px solid #b9c7d8;border-radius:10px;padding:12px;text-align:center;background:#fff}}
.flowbox{{min-height:82px}}
.cces{{min-height:190px}}
.big{{font-size:17px;font-weight:800}}
.legend{{font-size:9px;font-weight:800;margin-left:10px}}
.green{{color:#16a34a}} .blue{{color:#1677e8}} .orange{{color:#f59e0b}} .red{{color:#ef233c}} .gray{{color:#94a3b8}}
.flowrow{{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:center}}
.bus{{height:5px;background:#334155;border-radius:4px;margin:9px 0}}
.nbcard{{background:#fff;border:1px solid #b9c7d8;border-radius:11px;overflow:hidden}}
.nbhead{{padding:9px 10px;display:flex;align-items:center;gap:8px;font-size:13px}}
.nb0{{background:#ffd7d7}} .nb1{{background:#d8e9ff}} .nb2{{background:#dcfce7}} .nb3{{background:#fff0c2}} .nb4{{background:#eadcff}}
.house{{font-size:24px;font-weight:900}}
.nbhead small{{font-size:9px;color:#334155}}
.nbbody{{padding:9px 10px}}
.row{{display:flex;justify-content:space-between;gap:5px;font-size:9px;margin:8px 0}}
.row b{{font-size:9px}}
.badge{{display:block;border-radius:7px;text-align:center;padding:5px;font-size:9px;font-weight:800;margin:7px 0}}
.charge{{background:#dcfce7;color:#16a34a}} .discharge{{background:#dbeafe;color:#1677e8}} .idle{{background:#eef2f7;color:#64748b}}
.pf{{font-size:9px;font-weight:800;color:#64748b;margin-top:9px}}
.flowgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;text-align:center;margin-top:3px}}
.flowarrow{{font-size:25px;line-height:24px;font-weight:900}}
.flowgrid b{{display:block;font-size:8px}}
.flowgrid small{{display:block;font-size:7px;color:#64748b}}
.support{{background:#fff7ed;color:#c2410c;border-radius:6px;text-align:center;padding:4px;font-size:7px;font-weight:800;margin-top:7px}}
.chartbox{{background:#fff;border:1px solid #b9c7d8;border-radius:10px;padding:6px}}
.charttitle{{font-size:10px;font-weight:800;margin-left:5px}}
@media(max-width:1100px){{
 .gridtop,.main{{grid-template-columns:1fr}}
 .nbs,.charts{{grid-template-columns:repeat(2,1fr)}}
}}
</style>

<div class="dashboard">

<div class="main">
  <div>
    <div class="panel">
      <div class="title">Total Solar Generation</div>
      <div class="kv"><span>Total Rooftop Capacity</span><b>28 MW</b></div>
      <div class="kv"><span>Total Solar Generation</span><b>{total_solar:.1f} MW</b></div>
      <div class="bar orangebar"><i style="width:{min(100,total_solar/40*100):.1f}%"></i></div>
      <div style="text-align:right;font-size:9px;color:#64748b">{total_solar/40*100:.0f}% of 40 MW total capacity</div>
    </div>
    <div class="panel" style="margin-top:8px">
      <div class="title">Solar Farm (CCES Ground)</div>
      <div class="kv"><span>Total Capacity</span><b>12 MW</b></div>
