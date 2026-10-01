
import streamlit as st
import math, random, time
from datetime import datetime

st.set_page_config(
    page_title="Community Energy Management System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {padding: 1rem 1.2rem 2rem 1.2rem; max-width: 1550px;}
h1,h2,h3,h4,p {font-family: Arial, sans-serif;}
.panel {
    background:#ffffff;
    border:1px solid #b9c7d8;
    border-radius:14px;
    padding:14px 16px;
    margin-bottom:10px;
}
.title {font-size:22px;font-weight:800;color:#10243e;}
.sub {font-size:13px;font-weight:700;color:#64748b;}
.metric {font-size:20px;font-weight:800;color:#10243e;}
.small {font-size:11px;color:#64748b;}
.good {color:#16a34a;font-weight:800;}
.blue {color:#1677e8;font-weight:800;}
.orange {color:#f59e0b;font-weight:800;}
.bad {color:#ef233c;font-weight:800;}
.flowbox {
    background:#f8fafc;border:1px solid #b9c7d8;border-radius:12px;
    padding:12px;text-align:center;min-height:90px;
}
.nbcard {
    border:1px solid #b9c7d8;border-radius:12px;overflow:hidden;
    background:#fff;margin-bottom:8px;
}
.nbhead {padding:10px 12px;font-weight:800;font-size:15px;}
.nbbody {padding:10px 12px;}
.arrow {
    font-size:27px;font-weight:900;line-height:1;
    text-align:center;margin:3px 0;
}
.arrow-green {color:#16a34a;}
.arrow-blue {color:#1677e8;}
.arrow-orange {color:#f59e0b;}
.status {
    border-radius:8px;padding:5px 8px;font-size:11px;
    font-weight:800;text-align:center;
}
.charge {background:#dcfce7;color:#16a34a;}
.discharge {background:#dbeafe;color:#1677e8;}
.idle {background:#eef2f7;color:#64748b;}
.support {background:#fff7ed;color:#c2410c;border-radius:7px;
    padding:5px;font-size:9px;font-weight:800;text-align:center;}
.legend {
    display:inline-block;padding:4px 7px;border-radius:6px;
    margin-right:5px;font-size:10px;font-weight:800;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session state
# -----------------------------
defaults = {
    "running": False,
    "auto": True,
    "sim_time": 14.0,
    "speed": 1.0,
    "cces": 60.0,
    "bat": [random.uniform(.70,.95)*4 for _ in range(5)],
    "last_update": time.time()
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# Controls
# -----------------------------
st.markdown('<div class="title">⚡ Community Energy Management System</div>', unsafe_allow_html=True)
st.caption("5-neighbourhood renewable reliability simulation • Rooftop Solar + Li-ion + CCES")

top1, top2, top3 = st.columns([4.3, 3.2, 2.8])

with top1:
    st.markdown('<div class="panel"><div class="title" style="font-size:18px;">Environmental Conditions <span class="sub">(Affecting Solar Generation)</span></div>', unsafe_allow_html=True)
    irr = st.slider("☀ Solar Irradiance (W/m²)", 0, 1000, 800, 10)
    cloud = st.slider("☁ Cloud Cover (%)", 0, 100, 20)
    temp = st.slider("🌡 Ambient Temperature (°C)", 0, 50, 30)
    wind = st.slider("≋ Wind Speed (km/h)", 0, 50, 10)
    st.markdown("</div>", unsafe_allow_html=True)

with top2:
    st.markdown('<div class="panel"><div class="title" style="font-size:18px;">Time of Day</div>', unsafe_allow_html=True)
    t = st.session_state.sim_time
    st.progress(t/24)
    st.markdown(
        f"<div style='display:flex;justify-content:space-between;font-size:11px;font-weight:700;'>"
        f"<span>🌙 12 AM</span><span>☀️ 12 PM</span><span>🌙 12 AM</span></div>",
        unsafe_allow_html=True)
    h=int(t); m=int((t-h)*60); ap="AM" if h<12 else "PM"; dh=h%12 or 12
    time_text=f"{dh}:{m:02d} {ap}"
    state="DAYTIME – SOLAR GENERATION ACTIVE" if 5.5<=t<=18.5 else "NIGHT – STORAGE SUPPLY MODE"
    st.markdown(f"<h2 style='text-align:center;margin:5px 0'>{time_text}</h2><div style='text-align:center;background:#edf3f8;border-radius:8px;padding:5px;font-size:10px;font-weight:800;color:#64748b'>{state}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with top3:
    st.markdown('<div class="panel"><div class="title" style="font-size:18px;">Simulation Control</div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    if c1.button("Manual Control", use_container_width=True):
        st.session_state.auto=False
        st.rerun()
    if c2.button("Automatic Simulation", use_container_width=True):
        st.session_state.auto=True
        st.rerun()
    st.session_state.speed=st.slider("Simulation speed",0.5,5.0,st.session_state.speed,0.5)
    b1,b2,b3=st.columns(3)
    if b1.button("▶ Start", use_container_width=True):
        st.session_state.running=True
        st.rerun()
    if b2.button("Ⅱ Pause", use_container_width=True):
        st.session_state.running=False
        st.rerun()
    if b3.button("↻ Reset", use_container_width=True):
        st.session_state.running=False
        st.session_state.sim_time=14.0
        st.session_state.cces=60.0
        st.session_state.bat=[random.uniform(.70,.95)*4 for _ in range(5)]
        st.rerun()
    mode="AUTOMATIC" if st.session_state.auto else "MANUAL"
    status="RUNNING" if st.session_state.running else "PAUSED"
    st.markdown(f"<div class='small'>Mode: <b>{mode}</b> &nbsp; • &nbsp; <b>{status}</b></div></div>",unsafe_allow_html=True)

# -----------------------------
# Simulation model
# -----------------------------
def daylight(t):
    if 5.5 <= t <= 18.5:
        return max(0, math.sin(math.pi*(t-5.5)/13))
    return 0

def solar_factor():
    d=daylight(st.session_state.sim_time)
    cloud_factor=max(0,1-.65*cloud/100)
    temp_factor=max(.82,1-max(0,temp-25)*.004)
    return d*(irr/1000)*cloud_factor*temp_factor

def values():
    f=solar_factor()
    total=28*f
    solar=[total*x for x in [.185,.171,.218,.179,.197]]
    ground=12*f
    base=[4.6,4.0,4.4,4.3,4.1]
    t=st.session_state.sim_time
    if t<6:k=.72
    elif t<10:k=.82
    elif t<16:k=.68
    elif t<19:k=.90
    else:k=1.10
    mult=[1,.94,1.06,.98,1.03]
    demand=[base[i]*k*mult[i] for i in range(5)]
    return solar,ground,demand

def battery_status(i,solar,demand):
    b=st.session_state.bat[i]
    if solar>demand+.05 and b<3.97:return "charging"
    if demand>solar+.05 and b>.40:return "discharging"
    return "idle"

def simulate_step():
    if st.session_state.auto:
        st.session_state.sim_time=(st.session_state.sim_time+.15*st.session_state.speed)%24

    solar,ground,demand=values()
    dt=.0833*st.session_state.speed
    bat=st.session_state.bat[:]
    status=["idle"]*5
    transfer=[0]*5
    ccharge=0.0
    cdis=0.0

    surplus=[max(0,solar[i]-demand[i]) for i in range(5)]
    deficit=[max(0,demand[i]-solar[i]) for i in range(5)]

    # Local solar -> local load. Surplus -> local Li-ion.
    for i in range(5):
        if surplus[i]>0:
            room=4-bat[i]
            p=min(surplus[i],1.2)
            e=min(room,p*dt*.94)
            actual=e/max(dt*.94,1e-9)
            if room>.01:
                bat[i]+=e
                status[i]="charging"
                surplus[i]-=actual
            if surplus[i]>0:
                ccharge+=surplus[i]

    # Local Li-ion -> local load.
    for i in range(5):
        if deficit[i]>0:
            available=max(0,bat[i]-.4)
            p=min(deficit[i],1.5,available/max(dt,1e-9)*.95)
            if p>0:
                bat[i]-=p*dt/.95
                deficit[i]-=p
                status[i]="discharging"

    # Other neighbourhood Li-ion -> shortage neighbourhood.
    donors=[i for i in range(5) if bat[i]>.70*4]
    for r in range(5):
        if deficit[r]<=.05: continue
        for d in donors:
            if d==r: continue
            available=max(0,bat[d]-.50*4)
            p=min(deficit[r],1.0,available/max(dt,1e-9)*.92)
            if p>.01:
                bat[d]-=p*dt/.92
                bat[r]+=p*dt*.92
                transfer[r]+=p
                transfer[d]-=p
                deficit[r]-=p

    # Remaining shortage -> CCES.
    remain=sum(deficit)
    if remain>.01:
        p=min(remain,8)
        e=min(p*dt/.85,max(0,st.session_state.cces-5))
        cdis=e/max(dt,1e-9)*.85
        st.session_state.cces-=e

    # Ground solar + remaining excess -> CCES.
    ccharge += ground
    if ccharge>0:
        room=80-st.session_state.cces
        e=min(room,ccharge*dt*.85)
        st.session_state.cces+=e
        ccharge=e/max(dt,1e-9)/.85

    st.session_state.bat=[max(0,min(4,x)) for x in bat]
    st.session_state.cces=max(0,min(80,st.session_state.cces))
    return {"solar":solar,"ground":ground,"demand":demand,
            "status":status,"transfer":transfer,
            "cces_charge":ccharge,"cces_discharge":cdis}

data=simulate_step() if st.session_state.running else {
    "solar":values()[0],"ground":values()[1],"demand":values()[2],
    "status":[battery_status(i,values()[0][i],values()[2][i]) for i in range(5)],
    "transfer":[0]*5,"cces_charge":0,"cces_discharge":0
}

# -----------------------------
# Main flow diagram
# -----------------------------
left,mid,right=st.columns([2.2,6.4,2.5])

with left:
    st.markdown('<div class="panel"><div class="title" style="font-size:17px;">Rooftop Solar (All Houses)</div>',unsafe_allow_html=True)
    rt=sum(data["solar"])
    st.metric("Total Capacity","28 MW")
    st.metric("Current Generation",f"{rt:.1f} MW")
    st.progress(min(1,rt/28))
    st.markdown("<div class='good'>Distributed rooftop PV</div><div class='small'>Local solar → local demand<br>Excess → Li-ion → CCES</div>",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="title" style="font-size:17px;">Solar Farm (CCES Ground)</div>',unsafe_allow_html=True)
    st.metric("Total Capacity","12 MW")
    st.metric("Current Generation",f"{data['ground']:.1f} MW")
    st.progress(min(1,data["ground"]/12))
    st.markdown("</div>",unsafe_allow_html=True)

with mid:
    st.markdown('<div class="panel"><div class="title" style="font-size:18px;">Power Flow Diagram (Real-time)</div>',unsafe_allow_html=True)
    st.markdown(
        "<span class='legend' style='background:#dcfce7;color:#16a34a'>GREEN: Solar → load / charging</span>"
        "<span class='legend' style='background:#dbeafe;color:#1677e8'>BLUE: CCES → neighbourhood</span>"
        "<span class='legend' style='background:#fef3c7;color:#c2410c'>ORANGE: Li-ion → / charging CCES</span>",
        unsafe_allow_html=True)

    a,b,c3=st.columns([1.2,1.5,1.2])
    with a:
        st.markdown("<div class='flowbox'>☀️<br><b>Rooftop Solar</b><br>28 MW capacity</div>",unsafe_allow_html=True)
        st.markdown(f"<div class='arrow arrow-green'>↓ {rt:.1f} MW</div>",unsafe_allow_html=True)
        st.markdown("<div class='flowbox'>☀️<br><b>Ground Solar</b><br>12 MW capacity</div>",unsafe_allow_html=True)
    with b:
        st.markdown("<div class='flowbox' style='min-height:210px;'>🛢️<br><b>Central Energy Station</b><br>CCES<br><br><b>80 MWh</b><br>",unsafe_allow_html=True)
        st.progress(st.session_state.cces/80)
        st.markdown(f"<b>{st.session_state.cces:.1f}/80 MWh ({st.session_state.cces/80*100:.0f}%)</b></div>",unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='flowbox'>⚡<br><b>Distribution Bus</b><br>5 neighbourhood substations</div>",unsafe_allow_html=True)
        st.markdown("<div class='arrow arrow-blue'>↓ ↑</div>",unsafe_allow_html=True)
        st.markdown("<div class='small' style='text-align:center;'>Bidirectional energy flow</div>",unsafe_allow_html=True)

    st.divider()
    nb_cols=st.columns(5)
    for i,col in enumerate(nb_cols):
        stt=data["status"][i]
        arrow="↑" if stt=="charging" else "↓" if stt=="discharging" else "•"
        col.markdown(f"<div style='background:{NB_COLORS[i]};border:1px solid #b9c7d8;border-radius:10px;padding:9px;text-align:center'><b>NB {i+1}</b><br>4,000 conn.<br><span class='arrow {'arrow-orange' if stt=='charging' else 'arrow-blue' if stt=='discharging' else ''}'>{arrow}</span></div>",unsafe_allow_html=True)

    if sum(data["solar"])+data["ground"] > sum(data["demand"]):
        msg="☀️ SURPLUS: local demand supplied → Li-ion charging → CCES receives remaining excess"
        st.success(msg)
    else:
        st.info("⚡ SHORTAGE: local Li-ion responds → other NB Li-ion support if needed → CCES supplies remaining demand")
    st.markdown("</div>",unsafe_allow_html=True)

with right:
    total_solar=sum(data["solar"])+data["ground"]
    total_demand=sum(data["demand"])
    st.markdown('<div class="panel"><div class="title" style="font-size:17px;">System Summary (Current)</div>',unsafe_allow_html=True)
    st.metric("Total Solar Generation",f"{total_solar:.1f} MW")
    st.metric("Total Demand",f"{total_demand:.1f} MW")
    st.metric("CCES Charging","ACTIVE" if data["cces_charge"]>.01 else "0 MW")
    st.metric("CCES Discharging","ACTIVE" if data["cces_discharge"]>.01 else "0 MW")
    st.write(f"**CCES SOC:** {st.session_state.cces:.1f} / 80 MWh")
    st.progress(st.session_state.cces/80)
    totalbat=sum(st.session_state.bat)
    st.write(f"**Total Li-ion:** {totalbat:.1f} / 20 MWh")
    st.progress(totalbat/20)
    st.markdown("</div>",unsafe_allow_html=True)

# -----------------------------
# Neighbourhood cards
# -----------------------------
st.markdown("### Neighbourhood Status")
cols=st.columns(5)
for i,col in enumerate(cols):
    solar_i=data["solar"][i]; dem_i=data["demand"][i]
    bat_i=st.session_state.bat[i]; frac=bat_i/4
    status=data["status"][i]
    if status=="charging":
        badge='<div class="status charge">⚡ CHARGING</div>'
    elif status=="discharging":
        badge='<div class="status discharge">⚡ DISCHARGING</div>'
    else:
        badge='<div class="status idle">IDLE</div>'
    transfer=data["transfer"][i]
    with col:
        st.markdown(f'<div class="nbcard"><div class="nbhead" style="background:{NB_COLORS[i]}">🏠 Neighbourhood {i+1}<br><span class="small">4,000 consumers</span></div><div class="nbbody">',unsafe_allow_html=True)
        st.write(f"☀ **Rooftop Solar:** {solar_i:.1f} MW")
        st.write(f"▥ **Current Demand:** {dem_i:.1f} MW")
        st.write(f"🔋 **Li-ion:** {bat_i:.1f} / 4 MWh ({frac*100:.0f}%)")
        st.progress(frac)
        st.markdown(badge,unsafe_allow_html=True)

        if dem_i > solar_i:
            st.markdown(f"<div class='arrow arrow-blue'>↓</div><div class='small' style='text-align:center'><b>CCES / Li-ion → load</b></div>",unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='arrow arrow-green'>↑</div><div class='small' style='text-align:center'><b>Solar → battery / CCES</b></div>",unsafe_allow_html=True)

        if transfer[i] > .01:
            st.markdown("<div class='support'>← OTHER NB Li-ion SUPPORT</div>",unsafe_allow_html=True)
        elif transfer[i] < -.01:
            st.markdown("<div class='support'>OTHER NB Li-ion →</div>",unsafe_allow_html=True)
        st.markdown("</div></div>",unsafe_allow_html=True)

# -----------------------------
# Live profile section
# -----------------------------
st.markdown("### System Profiles")
p1,p2,p3,p4=st.columns(4)
with p1:
    st.metric("Solar",f"{total_solar:.1f} MW")
with p2:
    st.metric("Demand",f"{total_demand:.1f} MW")
with p3:
    st.metric("CCES",f"{st.session_state.cces:.1f} MWh")
with p4:
    st.metric("Li-ion",f"{sum(st.session_state.bat):.1f} MWh")

# Simple 24-hour reference curves, plus current marker.
hours=list(range(25))
solar_curve=[30*max(0,math.sin(math.pi*(h-5.5)/13)) if 5.5<=h<=18.5 else 0 for h in hours]
demand_curve=[8+7*max(0,math.sin(math.pi*(h-7)/14)) + 4*(1 if h>=18 else 0) for h in hours]
st.line_chart({"Solar generation (MW)":solar_curve,"Demand (MW)":demand_curve},height=240)

# -----------------------------
# Auto refresh
# -----------------------------
if st.session_state.running:
    time.sleep(max(0.08,0.45/st.session_state.speed))
    st.rerun()
