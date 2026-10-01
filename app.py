
import math, random, time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Community Energy Management System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# PAGE / CSS
# ============================================================
st.markdown("""
<style>
html, body, [class*="css"] {font-family:Arial,Helvetica,sans-serif;}
.block-container {max-width:1540px !important;padding:6px 8px 10px 8px !important;}
header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none;}

div[data-testid="stSlider"]{padding-top:0 !important;margin-top:-4px !important;margin-bottom:-9px !important;}
div[data-testid="stSlider"] label{font-size:10px !important;font-weight:700 !important;white-space:nowrap !important;}
div[data-testid="stSlider"] [data-testid="stSliderValue"]{font-size:10px !important;}
div[data-testid="stButton"] button{border-radius:8px !important;font-weight:700 !important;min-height:31px !important;padding:3px 5px !important;}
div[data-testid="stProgress"]{height:7px !important;}

.top-panel{border:1px solid #b9c7d8;border-radius:11px;background:#fff;padding:6px 12px 5px;box-sizing:border-box;}
.env-panel,.control-panel{height:43px;}
.top-title{font-size:17px;font-weight:800;color:#10243e;line-height:30px;}
.top-title span{font-size:12px;}
.env-units{display:grid;grid-template-columns:repeat(4,1fr);margin-top:0;color:#64748b;font-size:8px;text-align:center;}

.time-panel{
 height:126px;box-sizing:border-box;border:1px solid #7697bc;border-radius:11px;
 padding:7px 14px 8px;color:#fff;
 background:linear-gradient(135deg,#173b69 0%,#285f91 55%,#16365d 100%);
 box-shadow:0 2px 7px rgba(15,42,72,.15);
}
.time-title{font-size:17px;font-weight:800;line-height:22px;margin-bottom:5px;}
.time-track{position:relative;height:18px;border-radius:12px;background:linear-gradient(90deg,#182f58 0%,#58a5e5 35%,#ffd65a 50%,#58a5e5 65%,#182f58 100%);border:1px solid rgba(255,255,255,.45);}
.time-sun{position:absolute;left:50%;top:-8px;transform:translateX(-50%);font-size:18px;}
.time-marker{position:absolute;top:-3px;width:3px;height:24px;background:#fff;border-radius:2px;box-shadow:0 0 0 1px #173b69;}
.time-labels{display:flex;justify-content:space-between;font-size:9px;font-weight:700;margin-top:2px;}
.current-time{text-align:center;font-size:24px;font-weight:900;line-height:25px;margin-top:0;color:#fff;}
.time-state{margin:2px auto 0;width:65%;text-align:center;padding:3px 5px;border-radius:6px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.3);color:#fff;font-size:8px;font-weight:800;letter-spacing:.2px;}
.control-state{text-align:center;color:#64748b;font-size:9px;margin-top:4px;}

/* Main dashboard */
.dashboard{font-family:Arial,Helvetica,sans-serif;color:#10243e;background:#f4f7fb;}
.panel{background:#fff;border:1px solid #b9c7d8;border-radius:11px;padding:8px 10px;box-sizing:border-box;}
.main{display:grid;grid-template-columns:1.0fr 3.35fr 1.18fr;gap:7px;margin-top:5px;}
.nbs{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:6px;}
.charts{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px;}
.title{font-size:17px;font-weight:800;margin-bottom:7px;}
.sub{font-size:10px;color:#64748b;}
.kv{display:flex;justify-content:space-between;font-size:10px;margin:6px 0;}
.bar{height:8px;background:#e6edf5;border-radius:6px;overflow:hidden;margin:4px 0 6px;}
.bar i{display:block;height:100%;background:#16a34a;border-radius:6px;}
.orangebar i{background:#f59e0b;}.bluebar i{background:#1677e8;}
.solarbox,.flowbox{border:1px solid #b9c7d8;border-radius:9px;padding:9px;text-align:center;background:#fff;}
.flowbox{min-height:75px;}.cces{min-height:165px;}.big{font-size:16px;font-weight:800;}
.legend{font-size:8px;font-weight:800;margin-left:7px;}
.green{color:#16a34a}.blue{color:#1677e8}.orange{color:#f59e0b}.red{color:#ef233c}.gray{color:#94a3b8}
.flowrow{display:grid;grid-template-columns:1fr 1fr;gap:7px;align-items:center;}
.bus{height:4px;background:#334155;border-radius:4px;margin:7px 0;}
.nbcard{background:#fff;border:1px solid #b9c7d8;border-radius:10px;overflow:hidden;}
.nbhead{padding:7px 9px;display:flex;align-items:center;gap:7px;font-size:12px;}
.nb0{background:#ffd7d7}.nb1{background:#d8e9ff}.nb2{background:#dcfce7}.nb3{background:#fff0c2}.nb4{background:#eadcff}
.house{font-size:22px;font-weight:900;}.nbhead small{font-size:8px;color:#334155;}
.nbbody{padding:7px 9px;}.row{display:flex;justify-content:space-between;gap:4px;font-size:8px;margin:6px 0;}.row b{font-size:8px;}
.badge{display:block;border-radius:6px;text-align:center;padding:4px;font-size:8px;font-weight:800;margin:5px 0;}
.charge{background:#dcfce7;color:#16a34a}.discharge{background:#dbeafe;color:#1677e8}.idle{background:#eef2f7;color:#64748b}
.pf{font-size:8px;font-weight:800;color:#64748b;margin-top:7px;}
.flowgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;text-align:center;margin-top:2px;}
.flowarrow{font-size:22px;line-height:21px;font-weight:900;}.flowgrid b{display:block;font-size:7px;}.flowgrid small{display:block;font-size:6px;color:#64748b;}
.support{background:#fff7ed;color:#c2410c;border-radius:5px;text-align:center;padding:3px;font-size:6px;font-weight:800;margin-top:5px;}
.chartbox{background:#fff;border:1px solid #b9c7d8;border-radius:9px;padding:5px;}.charttitle{font-size:9px;font-weight:800;margin-left:4px;}
@media(max-width:1100px){.gridtop,.main{grid-template-columns:1fr}.nbs,.charts{grid-template-columns:repeat(2,1fr)}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "sim_time" not in st.session_state: st.session_state.sim_time = 0.0
if "running" not in st.session_state: st.session_state.running = False
if "auto" not in st.session_state: st.session_state.auto = True
if "speed" not in st.session_state: st.session_state.speed = 1.0
if "cces" not in st.session_state: st.session_state.cces = 55.0
if "bat" not in st.session_state:
    st.session_state.bat = [random.uniform(.70, .95) * 4 for _ in range(5)]
if "hist" not in st.session_state:
    st.session_state.hist = {"solar":[],"demand":[],"cces":[],"liion":[]}

# ============================================================
# TOP CONTROLS — compact single-screen layout
# ============================================================
c1, c2, c3 = st.columns([4.2, 3.25, 2.55], gap="small")

with c1:
    st.markdown("""
    <div class="top-panel env-panel">
      <div class="top-title">Environmental Conditions <span>(Affecting Solar Generation)</span></div>
    </div>
    """, unsafe_allow_html=True)

    e1, e2, e3, e4 = st.columns(4, gap="small")
    with e1:
        irr = st.slider("☀ Irradiance", 0, 1000, 800, 10)
    with e2:
        cloud = st.slider("☁ Cloud", 0, 100, 20, 1)
    with e3:
        temp = st.slider("🌡 Temp", 0, 50, 30, 1)
    with e4:
        wind = st.slider("≋ Wind", 0, 50, 10, 1)

    st.markdown("""
    <div class="env-units">
      <span>W/m²</span><span>%</span><span>°C</span><span>km/h</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    t = st.session_state.sim_time
    hh = int(t)
    mm = int((t-hh)*60)
    ap = "AM" if hh < 12 else "PM"
    dh = hh % 12 or 12
    day = 5.5 <= t <= 18.5

    st.markdown(f"""
    <div class="time-panel">
      <div class="time-title">Time of Day</div>
      <div class="time-track">
        <div class="time-sun">☀</div>
        <div class="time-marker" style="left:{(t/24)*100:.2f}%"></div>
      </div>
      <div class="time-labels">
        <span>☾ 12 AM</span>
        <span>☀ 12 PM</span>
        <span>☾ 12 AM</span>
      </div>
      <div class="current-time">{dh}:{mm:02d} {ap}</div>
      <div class="time-state">
        {"DAYTIME · SOLAR GENERATION ACTIVE" if day else "NIGHT · CCES SUPPLY MODE"}
      </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="top-panel control-panel">
      <div class="top-title">Simulation Control</div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.auto = True
    st.session_state.speed = st.slider(
        "Simulation Speed", .5, 5.0, st.session_state.speed, .5
    )

    b1, b2, b3 = st.columns(3, gap="small")
    with b1:
        if st.button("▶ Start", use_container_width=True):
            st.session_state.running = True
            st.rerun()
    with b2:
        if st.button("Ⅱ Pause", use_container_width=True):
            st.session_state.running = False
            st.rerun()
    with b3:
        if st.button("↻ Reset", use_container_width=True):
            st.session_state.running = False
            st.session_state.sim_time = 0.0
            st.session_state.cces = 55.0
            st.session_state.bat = [random.uniform(.70, .95) * 4 for _ in range(5)]
            st.session_state.hist = {"solar": [], "demand": [], "cces": [], "liion": []}
            st.rerun()

    st.markdown(f"""
    <div class="control-state">
      AUTOMATIC SIMULATION · <b>{"RUNNING" if st.session_state.running else "PAUSED"}</b>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SIMULATION
# ============================================================
def daylight(t):
    return math.sin(math.pi*(t-5.5)/13) if 5.5 <= t <= 18.5 else 0

def solar_factor():
    d=max(0,daylight(st.session_state.sim_time))
    cloud_factor=max(0,1-.65*cloud/100)
    temp_factor=max(.82,1-max(0,temp-25)*.004)
    return d*(irr/1000)*cloud_factor*temp_factor

def get_values():
    f=solar_factor()
    rooftop_total=28*f
    solar=[rooftop_total*x for x in [.185,.171,.218,.179,.197]]
    ground=12*f
    base=[4.6,4.0,4.4,4.3,4.1]
    t=st.session_state.sim_time
    k=.72 if t<6 else .82 if t<10 else .68 if t<16 else .90 if t<19 else 1.10
    mult=[1,.94,1.06,.98,1.03]
    demand=[base[i]*k*mult[i] for i in range(5)]
    return solar,ground,demand

def run_step():
    if st.session_state.auto:
        st.session_state.sim_time=(st.session_state.sim_time+.15*st.session_state.speed)%24

    solar,ground,demand=get_values()
    dt=.0833*st.session_state.speed
    bat=st.session_state.bat[:]
    status=["idle"]*5
    transfer=[0.0]*5
    ccharge=0.0
    cdis=0.0

    is_day = 5.5 <= st.session_state.sim_time <= 18.5

    # --------------------------------------------------------
    # DESIGN DEMO DISPATCH
    #
    # Day:
    #   Solar -> local demand
    #   surplus -> local Li-ion
    #   once Li-ion is full -> CCES
    #
    # Night:
    #   CCES supplies the main shortage
    #   only NB1 and NB3 receive a SMALL local Li-ion support
    #   event. This keeps the Li-ion SOC from falling rapidly.
    # --------------------------------------------------------

    if is_day:
        # Local solar serves local demand first.
        surplus=[max(0,solar[i]-demand[i]) for i in range(5)]
        deficit=[max(0,demand[i]-solar[i]) for i in range(5)]

        # Small local deficits are intentionally left to CCES.
        # Li-ion is NOT discharged merely because solar is lower than demand.
        for i in range(5):
            if surplus[i] > 0:
                room=max(0,4-bat[i])

                # Charge Li-ion first. Cap the demonstration charging power
                # so the visualisation clearly shows the battery filling.
                p=min(surplus[i],1.2)
                e=min(room,p*dt*.94)

                if e > 0.0001:
                    bat[i]+=e
                    surplus[i]-=e/max(dt*.94,1e-9)
                    status[i]="charging"

                # Once Li-ion is full, remaining solar goes to CCES.
                if surplus[i] > 0.01:
                    ccharge += surplus[i]

        # Ground solar goes directly toward CCES.
        ccharge += ground

        # Charge CCES only after Li-ion charging has been attempted.
        if ccharge > 0:
            room=max(0,80-st.session_state.cces)
            e=min(room,ccharge*dt*.85)
            st.session_state.cces+=e
            ccharge=e/max(dt*.85,1e-9)

        # Remaining daytime shortage is supplied by CCES.
        remaining=sum(deficit)
        if remaining > 0.01:
            p=min(remaining,8)
            e=min(p*dt/.85,max(0,st.session_state.cces-0.5))
            cdis=e/max(dt,1e-9)*.85
            st.session_state.cces-=e

    else:
        # NIGHT:
        # Create intentionally small local shortage events only in NB1/NB3.
        # These are visual/demo events, not full battery discharge.
        shortage_event=[0.22,0.0,0.18,0.0,0.0]

        for i in range(5):
            if shortage_event[i] > 0 and bat[i] > 0.60:
                # Only a small amount of the local Li-ion battery is used.
                p=min(shortage_event[i],0.35)
                e=min(max(0,bat[i]-0.60),p*dt/.95)
                if e > 0.0001:
                    bat[i]-=e
                    status[i]="discharging"

        # CCES is the main night-time source.
        # For the demo, the overnight energy reserve is deliberately
        # scheduled so that CCES reaches ~10% SOC at sunrise.
        #
        # This means the story is:
        # 12 AM -> CCES has useful stored energy
        # night -> CCES discharges
        # ~5:30 AM -> CCES reaches 10%
        # daytime -> Li-ion charges first, then CCES charges
        night_demand=sum(demand)

        liion_power=0
        for i in [0,2]:
            if status[i]=="discharging":
                liion_power += shortage_event[i]

        cces_power=max(0,night_demand-liion_power)

        if cces_power > 0.01:
            # Target 8 MWh (10%) at the start of daytime.
            target_soc=8.0

            if st.session_state.sim_time < 5.5:
                remaining_night_hours=max(0.15,5.5-st.session_state.sim_time)
                available_energy=max(0,st.session_state.cces-target_soc)

                # Discharge at the smaller of actual demand and the
                # scheduled power required to arrive at exactly 10%.
                scheduled_power=available_energy/remaining_night_hours
                p=min(cces_power,scheduled_power,12.0)

                e=min(p*dt/.85,max(0,st.session_state.cces-target_soc))
                cdis=e/max(dt,1e-9)*.85
                st.session_state.cces-=e
            else:
                # Daytime begins with the desired 10% reserve.
                st.session_state.cces=max(target_soc,st.session_state.cces)

        # If one of the non-event neighbourhoods is exceptionally short,
        # CCES still handles it; their Li-ion is intentionally preserved.

    # --------------------------------------------------------
    # OPTIONAL CROSS-NEIGHBOUR SUPPORT
    # Only active if NB1/NB3 event exceeds their local Li-ion response.
    # In the normal demo this remains zero, which makes the dashboard
    # easier to understand.
    # --------------------------------------------------------
    if not is_day:
        for target in [0,2]:
            if status[target]=="discharging" and bat[target] < 0.75:
                donors=[j for j in range(5) if j not in [0,2] and bat[j] > 3.2]
                if donors:
                    donor=donors[0]
                    transfer[target]+=0.05
                    transfer[donor]-=0.05

    st.session_state.bat=[max(0,min(4,x)) for x in bat]
    st.session_state.cces=max(0,min(80,st.session_state.cces))

    st.session_state.hist["solar"].append(sum(solar)+ground)
    st.session_state.hist["demand"].append(sum(demand))
    st.session_state.hist["cces"].append(st.session_state.cces)
    st.session_state.hist["liion"].append(sum(st.session_state.bat))
    for k in st.session_state.hist:
        st.session_state.hist[k]=st.session_state.hist[k][-96:]

    return {"solar":solar,"ground":ground,"demand":demand,
            "status":status,"transfer":transfer,
            "cces_charge":ccharge,"cces_discharge":cdis}

if st.session_state.running:
    data=run_step()
else:
    solar,ground,demand=get_values()
    data={"solar":solar,"ground":ground,"demand":demand,
          "status":["idle"]*5,"transfer":[0]*5,
          "cces_charge":0,"cces_discharge":0}

# ============================================================
# HTML DASHBOARD
# This is deliberately built to mirror the supplied reference:
# left solar panels | central flow | right summary
# then 5 neighbourhood cards | four 24-hour charts.
# ============================================================
def esc(x):
    return str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

solar=data["solar"]; ground=data["ground"]; demand=data["demand"]
total_solar=sum(solar)+ground; total_demand=sum(demand)
total_bat=sum(st.session_state.bat)

def battery_badge(i):
    s=data["status"][i]
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
    w,h=360,145
    left,top=36,26
    pw,ph=306,94
    pts=[]
    for j,v in enumerate(vals):
        x=left+(j/max(1,len(vals)-1))*pw
        y=top+ph-(max(0,min(ymax,v))/ymax)*ph
        pts.append(f"{x:.1f},{y:.1f}")
    poly=" ".join(pts)
    return f"""
    <div class="chartbox">
      <div class="charttitle">{title}</div>
      <svg viewBox="0 0 {w} {h}" width="100%" height="145">
        <line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" stroke="#dbe4ee"/>
        <line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#dbe4ee"/>
        <polyline points="{poly}" fill="none" stroke="{color}" stroke-width="3"/>
        <text x="{left}" y="138" font-size="9" fill="#64748b">12 AM</text>
        <text x="{left+pw/2}" y="138" font-size="9" fill="#64748b" text-anchor="middle">12 PM</text>
        <text x="{left+pw}" y="138" font-size="9" fill="#64748b" text-anchor="end">12 AM</text>
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
      <div class="kv"><span>Current Generation</span><b>{ground:.1f} MW</b></div>
      <div class="bar"><i style="width:{ground/12*100:.1f}%"></i></div>
      <div style="text-align:right;font-size:9px;color:#64748b">{ground/12*100:.0f}%</div>
    </div>
  </div>

  <div class="panel">
    <div class="title">Power Flow Diagram (Real-time)
      <span class="legend green">━━► Solar</span>
      <span class="legend blue">━━► CCES → NB</span>
      <span class="legend orange">━━► Li-ion</span>
    </div>

    <div class="flowrow">
      <div>
        <div class="flowbox"><div style="font-size:28px">☀️</div><b>Rooftop Solar</b><br><span class="sub">28 MW capacity</span></div>
        <div class="flowarrow green">→ {sum(solar):.1f} MW</div>
        <div class="flowbox"><div style="font-size:28px">☀️</div><b>Solar Farm</b><br><span class="sub">12 MW capacity</span></div>
      </div>
      <div class="flowbox cces">
        <div class="big">Central Energy Station</div>
        <div class="sub">(CCES)</div>
        <div style="font-size:50px;margin-top:8px">🛢️</div>
        <b>CCES 80 MWh</b>
        <div class="bar"><i style="width:{st.session_state.cces/80*100:.1f}%"></i></div>
        <b>{st.session_state.cces:.1f} / 80 MWh ({st.session_state.cces/80*100:.0f}%)</b>
      </div>
    </div>

    <div class="bus"></div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:5px">
      {''.join(f'<div class="solarbox"><b>NB {i+1}</b><br><span class="sub">4,000 consumers</span><br><span class="flowarrow {"blue" if data["status"][i]=="discharging" else "orange" if data["status"][i]=="charging" else "gray"}">{"↓" if data["status"][i]=="discharging" else "↑" if data["status"][i]=="charging" else "•"}</span></div>' for i in range(5))}
    </div>
    <div style="margin-top:9px;padding:7px;background:#f8fafc;border-radius:7px;text-align:center;font-size:9px;font-weight:800">
      {"☀ SURPLUS: Solar → local demand → Li-ion → CCES" if total_solar>total_demand else "⚡ NIGHT: CCES supplies main load • NB1/NB3 Li-ion handles small local shortage"}
    </div>
  </div>

  <div class="panel">
    <div class="title">System Summary (Current)</div>
    <div class="kv"><span>Total Solar Generation</span><b>{total_solar:.1f} MW</b></div>
    <div class="kv"><span>Total Demand</span><b>{total_demand:.1f} MW</b></div>
    <div class="kv"><span>Charging CCES</span><b class="green">{data["cces_charge"]:.1f} MW</b></div>
    <div class="kv"><span>Discharging CCES</span><b class="blue">{data["cces_discharge"]:.1f} MW</b></div>
    <div class="kv"><span>CCES State of Charge</span><b>{st.session_state.cces:.1f}/80 MWh</b></div>
    <div class="bar"><i style="width:{st.session_state.cces/80*100:.1f}%"></i></div>
    <div class="kv"><span>Total Li-ion Charge</span><b>{total_bat:.1f}/20 MWh</b></div>
    <div class="bar bluebar"><i style="width:{total_bat/20*100:.1f}%"></i></div>
  </div>
</div>

<div class="nbs">{nb_html}</div>

<div class="charts">
{chart_svg("Total Solar Generation (MW)",hist_s,"#f59e0b",40,"MW")}
{chart_svg("Total Demand (MW)",hist_d,"#ef233c",30,"MW")}
{chart_svg("CCES State of Charge (MWh)",hist_c,"#16a34a",80,"MWh")}
{chart_svg("Total Li-ion State of Charge (MWh)",hist_l,"#1677e8",20,"MWh")}
</div>
</div>
"""

components.html(html,height=620,scrolling=False)

# Automatic refresh.
if st.session_state.running:
    time.sleep(max(0.08,0.35/st.session_state.speed))
    st.rerun()
