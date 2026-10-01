
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
.block-container {max-width:1540px !important;padding:78px 10px 14px 10px !important;}
header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none;}

div[data-testid="stSlider"]{padding-top:0 !important;margin-top:2px !important;margin-bottom:-4px !important;}
div[data-testid="stSlider"] label{font-size:8px !important;font-weight:700 !important;white-space:nowrap !important;}
div[data-testid="stSlider"] [data-testid="stSliderValue"]{font-size:10px !important;}
div[data-testid="stButton"] button{border-radius:8px !important;font-weight:700 !important;min-height:27px !important;padding:2px 4px !important;}
div[data-testid="stProgress"]{height:7px !important;}

.top-panel{border:1px solid #b9c7d8;border-radius:9px;background:#fff;padding:4px 9px 3px;box-sizing:border-box;}
.env-panel,.control-panel{height:40px;}
.top-title{font-size:14px;font-weight:800;color:#10243e;line-height:29px;}
.top-title span{font-size:10px;}
.env-units{display:grid;grid-template-columns:repeat(4,1fr);margin-top:0;color:#64748b;font-size:8px;text-align:center;}

.time-panel{
 height:104px;box-sizing:border-box;border:1px solid #7697bc;border-radius:9px;
 padding:5px 11px 6px;color:#fff;
 background:linear-gradient(135deg,#173b69 0%,#285f91 55%,#16365d 100%);
 box-shadow:0 2px 7px rgba(15,42,72,.15);
}
.time-title{font-size:14px;font-weight:800;line-height:18px;margin-bottom:3px;}
.time-track{position:relative;height:14px;border-radius:12px;background:linear-gradient(90deg,#182f58 0%,#58a5e5 35%,#ffd65a 50%,#58a5e5 65%,#182f58 100%);border:1px solid rgba(255,255,255,.45);}
.time-sun{position:absolute;left:50%;top:-7px;transform:translateX(-50%);font-size:15px;}
.time-marker{position:absolute;top:-3px;width:3px;height:20px;background:#fff;border-radius:2px;box-shadow:0 0 0 1px #173b69;}
.time-labels{display:flex;justify-content:space-between;font-size:8px;font-weight:700;margin-top:2px;}
.current-time{text-align:center;font-size:21px;font-weight:900;line-height:22px;margin-top:0;color:#fff;}
.time-state{margin:1px auto 0;width:62%;text-align:center;padding:3px 5px;border-radius:6px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.3);color:#fff;font-size:7px;font-weight:800;letter-spacing:.1px;}
.control-state{text-align:center;color:#64748b;font-size:8px;margin-top:2px;}
.summary-time{
    margin-top:12px;
    padding:10px 8px 9px;
    border-radius:9px;
    border:1px solid #7697bc;
    background:linear-gradient(135deg,#173b69 0%,#285f91 55%,#16365d 100%);
    text-align:center;
    color:#fff;
}
.summary-time-label{
    font-size:8px;
    font-weight:800;
    letter-spacing:.8px;
    color:rgba(255,255,255,.82);
}
.summary-time-value{
    font-size:24px;
    line-height:27px;
    font-weight:900;
    margin-top:1px;
    color:#fff;
}
.summary-time-state{
    display:inline-block;
    margin-top:3px;
    padding:3px 8px;
    border-radius:5px;
    background:rgba(255,255,255,.17);
    border:1px solid rgba(255,255,255,.28);
    font-size:7px;
    font-weight:800;
}


/* Main dashboard */
.dashboard{font-family:Arial,Helvetica,sans-serif;color:#10243e;background:#f4f7fb;}
.panel{background:#fff;border:1px solid #b9c7d8;border-radius:11px;padding:8px 10px;box-sizing:border-box;}
.main{display:grid;grid-template-columns:1.0fr 3.35fr 1.18fr;gap:7px;margin-top:5px;}
.nbs{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:6px;}
.charts{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px;}
.title{font-size:17px;font-weight:800;margin-bottom:7px;}
.sub{font-size:10px;color:#64748b;}
.kv{display:flex;justify-content:space-between;font-size:10px;margin:6px 0;}
.bar{height:6px;background:#e6edf5;border-radius:6px;overflow:hidden;margin:4px 0 6px;}
.bar i{display:block;height:100%;background:#16a34a;border-radius:6px;}
.orangebar i{background:#f59e0b;}.bluebar i{background:#1677e8;}
.solarbox,.flowbox{border:1px solid #b9c7d8;border-radius:8px;padding:6px;text-align:center;background:#fff;}
.flowbox{min-height:62px;}.cces{min-height:140px;}.big{font-size:16px;font-weight:800;}
.legend{font-size:8px;font-weight:800;margin-left:7px;}
.green{color:#16a34a}.blue{color:#1677e8}.orange{color:#f59e0b}.red{color:#ef233c}.gray{color:#94a3b8}
.flowrow{display:grid;grid-template-columns:1fr 1fr;gap:7px;align-items:center;}
.bus{height:4px;background:#334155;border-radius:4px;margin:7px 0;}
.nbcard{background:#fff;border:1px solid #b9c7d8;border-radius:10px;overflow:hidden;}
.nbhead{padding:5px 7px;display:flex;align-items:center;gap:7px;font-size:12px;}
.nb0{background:#ffd7d7}.nb1{background:#d8e9ff}.nb2{background:#dcfce7}.nb3{background:#fff0c2}.nb4{background:#eadcff}
.house{font-size:22px;font-weight:900;}.nbhead small{font-size:8px;color:#334155;}
.nbbody{padding:5px 7px;}.row{display:flex;justify-content:space-between;gap:4px;font-size:8px;margin:6px 0;}.row b{font-size:8px;}
.badge{display:block;border-radius:6px;text-align:center;padding:4px;font-size:8px;font-weight:800;margin:5px 0;}
.charge{background:#dcfce7;color:#16a34a}.discharge{background:#dbeafe;color:#1677e8}.idle{background:#eef2f7;color:#64748b}
.pf{font-size:8px;font-weight:800;color:#64748b;margin-top:7px;}
.flowgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;text-align:center;margin-top:2px;}
.flowarrow{font-size:18px;line-height:18px;font-weight:900;}.flowgrid b{display:block;font-size:7px;}.flowgrid small{display:block;font-size:6px;color:#64748b;}
.support{background:#fff7ed;color:#c2410c;border-radius:5px;text-align:center;padding:3px;font-size:6px;font-weight:800;margin-top:5px;}
.chartbox{background:#fff;border:1px solid #b9c7d8;border-radius:9px;padding:5px;}.charttitle{font-size:9px;font-weight:800;margin-left:4px;}
/* Keep the top controls in one horizontal band on desktop. */
div[data-testid="stHorizontalBlock"]{
    flex-wrap:nowrap !important;
    align-items:stretch !important;
}
div[data-testid="stHorizontalBlock"] > div{
    min-width:0 !important;
}
.top-panel,.time-panel{
    overflow:visible;
}
@media(max-width:1100px){
 .gridtop,.main{grid-template-columns:1fr}
 .nbs,.charts{grid-template-columns:repeat(2,1fr)}
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "sim_time" not in st.session_state: st.session_state.sim_time = 0.0
if "running" not in st.session_state: st.session_state.running = False
if "auto" not in st.session_state: st.session_state.auto = True
if "speed" not in st.session_state: st.session_state.speed = 1.0
if "sim_day" not in st.session_state: st.session_state.sim_day = 0
if "night_start_target" not in st.session_state: st.session_state.night_start_target = 55.0
if "sunrise_target" not in st.session_state: st.session_state.sunrise_target = 8.0
if "cces" not in st.session_state: st.session_state.cces = 55.0
if "bat" not in st.session_state:
    st.session_state.bat = [random.uniform(.70, .95) * 4 for _ in range(5)]
if "hist" not in st.session_state:
    st.session_state.hist = {"solar":[],"demand":[],"cces":[],"liion":[]}

def reset_simulation():
    """Restore the complete simulation to its initial state."""
    st.session_state.running = False
    st.session_state.sim_time = 0.0
    st.session_state.sim_day = 0
    st.session_state.night_start_target = 55.0
    st.session_state.sunrise_target = 8.0
    st.session_state.cces = 55.0
    st.session_state.bat = [random.uniform(.70, .95) * 4 for _ in range(5)]
    st.session_state.hist = {"solar": [], "demand": [], "cces": [], "liion": []}

    # Explicitly reset the environmental sliders too.
    st.session_state.irr_slider = 800
    st.session_state.cloud_slider = 20
    st.session_state.temp_slider = 30
    st.session_state.wind_slider = 10

# ============================================================
# TOP CONTROLS — fixed compact 16:9 presentation band
# ============================================================
c1, c2, c3 = st.columns([4.25, 3.15, 2.60], gap="small")

with c1:
    st.markdown("""
    <div class="top-panel env-panel">
      <div class="top-title">Environmental Conditions <span>(Affecting Solar Generation)</span></div>
    </div>
    """, unsafe_allow_html=True)
    e1, e2, e3, e4 = st.columns(4, gap="small")
    with e1:
        irr = st.slider("☀ Irradiance", 0, 1000, 800, 10, key="irr_slider")
    with e2:
        cloud = st.slider("☁ Cloud", 0, 100, 20, 1, key="cloud_slider")
    with e3:
        temp = st.slider("🌡 Temperature", 0, 50, 30, 1, key="temp_slider")
    with e4:
        wind = st.slider("≋ Wind", 0, 50, 10, 1, key="wind_slider")

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
      <div class="time-labels"><span>☾ 12 AM</span><span>☀ 12 PM</span><span>☾ 12 AM</span></div>
      <div class="current-time">{dh}:{mm:02d} {ap}</div>
      <div class="time-state">{"DAY · SOLAR ACTIVE" if day else "NIGHT · CCES SUPPLY"}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="top-panel control-panel">
      <div class="top-title">Simulation Control</div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.auto = True
    st.session_state.speed = st.slider("Simulation Speed", .5, 5.0, st.session_state.speed, .5)

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
        st.button(
            "↻ Reset",
            use_container_width=True,
            on_click=reset_simulation
        )

    st.markdown(f'<div class="control-state">AUTO · <b>{"RUNNING" if st.session_state.running else "PAUSED"}</b></div>', unsafe_allow_html=True)

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
    rooftop_total=32*f
    solar=[rooftop_total*x for x in [.185,.171,.218,.179,.197]]
    ground=14*f
    base=[4.6,4.0,4.4,4.3,4.1]
    t=st.session_state.sim_time
    k=.72 if t<6 else .82 if t<10 else .68 if t<16 else .90 if t<19 else 1.10
    mult=[1,.94,1.06,.98,1.03]
    demand=[base[i]*k*mult[i] for i in range(5)]
    return solar,ground,demand

def run_step():
    # Advance the simulation clock. Energy changes are calculated from the
    # actual solar surplus/deficit at this timestep -- no artificial SOC jumps.
    old_time = st.session_state.sim_time
    time_step = .15 * st.session_state.speed
    new_time = old_time + time_step
    if new_time >= 24:
        st.session_state.sim_day += 1
        new_time %= 24

    st.session_state.sim_time = new_time

    solar, ground, demand = get_values()
    dt = time_step
    bat = st.session_state.bat[:]
    status = ["idle"] * 5
    transfer = [0.0] * 5
    ccharge = 0.0
    cdis = 0.0

    is_day = 5.5 <= st.session_state.sim_time <= 18.5

    if is_day:
        # Solar directly serves each neighbourhood first.
        surplus = [max(0.0, solar[i] - demand[i]) for i in range(5)]
        deficit = [max(0.0, demand[i] - solar[i]) for i in range(5)]

        # Only small daytime fluctuations are handled by Li-ion.
        for i in range(5):
            if deficit[i] > 0.01 and bat[i] > 3.65:
                p = min(deficit[i], 0.12)
                e = min(bat[i] - 3.65, p * dt / .97)
                if e > 0.0001:
                    bat[i] -= e
                    status[i] = "discharging"

        # Solar surplus charges Li-ion first.
        available_surplus = sum(surplus) + ground
        for i in range(5):
            if available_surplus > 0.01 and bat[i] < 4.0:
                room = 4.0 - bat[i]
                p = min(available_surplus, 2.5)
                e = min(room, p * dt * .95)
                if e > 0.0001:
                    bat[i] += e
                    available_surplus -= e / max(dt * .95, 1e-9)
                    status[i] = "charging"

        # ----------------------------------------------------
        # CCES: ONLY REAL SOLAR SURPLUS CHARGES IT.
        #
        # There is deliberately NO target-SOC interpolation and NO
        # "fill to 80 MWh at 5 PM" command. Under default conditions,
        # the modeled solar resource is sized so the real surplus
        # gradually raises CCES to ~80 MWh by around 5 PM.
        #
        # Changing irradiance/cloud cover therefore directly changes
        # the CCES charging rate and final SOC.
        # ----------------------------------------------------
        if available_surplus > 0.01 and st.session_state.cces < 80.0:
            charge_power = min(available_surplus, 8.0)  # MW compressor limit
            e = min(80.0 - st.session_state.cces, charge_power * dt * .90)
            if e > 0.0001:
                st.session_state.cces += e
                ccharge = e / max(dt * .90, 1e-9)

    else:
        # Night: CCES is the primary source.
        # NB1/NB3 provide only small local fluctuations.
        shortage_event = [0.18, 0.0, 0.15, 0.0, 0.0]

        for i in range(5):
            if shortage_event[i] > 0 and bat[i] > 3.60:
                p = min(shortage_event[i], 0.20)
                e = min(bat[i] - 3.60, p * dt / .97)
                if e > 0.0001:
                    bat[i] -= e
                    status[i] = "discharging"

        # Keep the intended daily operating envelope, but never create
        # energy: CCES follows a discharge trajectory only when it has
        # enough stored energy. If poor weather left less energy stored,
        # the SOC remains lower rather than magically jumping back up.
        t = st.session_state.sim_time
        night_start = 80.0
        midnight_target = 55.0

        if t >= 18.5:
            frac = (t - 18.5) / 5.5
            desired_soc = night_start + (midnight_target - night_start) * max(0.0, min(1.0, frac))
        else:
            frac = t / 5.5
            desired_soc = midnight_target + (8.0 - midnight_target) * max(0.0, min(1.0, frac))

        available_to_discharge = max(0.0, st.session_state.cces - desired_soc)
        if available_to_discharge > 0.0001:
            e = min(available_to_discharge, 12.0 * dt)
            st.session_state.cces -= e
            cdis = e / max(dt, 1e-9) * .85

    # Physical bounds only. No end-of-day SOC correction.
    st.session_state.bat = [max(0.0, min(4.0, x)) for x in bat]
    st.session_state.cces = max(0.0, min(80.0, st.session_state.cces))

    st.session_state.hist["solar"].append(sum(solar) + ground)
    st.session_state.hist["demand"].append(sum(demand))
    st.session_state.hist["cces"].append(st.session_state.cces)
    st.session_state.hist["liion"].append(sum(st.session_state.bat))

    for k in st.session_state.hist:
        st.session_state.hist[k] = st.session_state.hist[k][-96:]

    return {
        "solar": solar,
        "ground": ground,
        "demand": demand,
        "status": status,
        "transfer": transfer,
        "cces_charge": ccharge,
        "cces_discharge": cdis
    }

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

    <div class="summary-time">
      <div class="summary-time-label">SIMULATION TIME</div>
      <div class="summary-time-value">{dh}:{mm:02d} {ap}</div>
      <div class="summary-time-state">
        {"☀ DAY · SOLAR ACTIVE" if day else "☾ NIGHT · CCES SUPPLY"}
      </div>
    </div>
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

components.html(html,height=900,scrolling=False)

# Automatic refresh.
if st.session_state.running:
    time.sleep(max(0.08,0.35/st.session_state.speed))
    st.rerun()
