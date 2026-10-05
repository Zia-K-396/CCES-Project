
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
