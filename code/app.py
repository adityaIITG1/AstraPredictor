
import streamlit as st, pandas as pd, numpy as np, plotly.express as px, plotly.io as pio, plotly.graph_objects as go
import joblib, os, json
from datetime import datetime
from cryptography.fernet import Fernet

# ---- Theme settings ----
army_green="#355E3B"
accent="#E94560"
pb_cols=["#118DFF","#E94560","#6B4FA3","#32C6A6"]
template=go.layout.Template(layout=dict(colorway=pb_cols,
    font=dict(family="Segoe UI, sans-serif",size=12,color="#222"),
    paper_bgcolor="#FFFFFF",plot_bgcolor="#FFFFFF",margin=dict(l=40,r=20,t=60,b=40)))
pio.templates["army"]=template
pio.templates.default="army"

# ---- Page Config ----
st.set_page_config(page_title="AstraPredictor 2.0",layout="wide")

# ---- CSS ----
st.markdown(f'''
<style>
.stApp {{background:linear-gradient(135deg,#f5f7fa 0%,#dfe6ec 100%);}}
.top {{background:{army_green};color:white;padding:0.6rem 1rem;border-radius:6px;font-size:20px;font-weight:600;}}
.metric {{padding:1rem;border-radius:8px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,0.12);text-align:center;}}
.metric h4{{margin:0;color:#666;}}
.metric h2{{margin:4px 0 0 0;font-size:32px;font-weight:700;}}
.dark .metric{{background:#2c2c2c;}}
.dark .stApp{{background:#1e1e1e;}}
</style>
''',unsafe_allow_html=True)

st.markdown("<div class='top'>🪖 AstraPredictor&nbsp;2.0 | AI Military Supply Forecaster | 🇮🇳 Jai Hind</div>",unsafe_allow_html=True)

# ---- Sidebar ----
with st.sidebar:
    st.header("Mission Parameters")
    # template quick-select
    with open(os.path.join('code','assets','mission_templates.json'),'r') as f:
        templates=json.load(f)
    template_name=st.selectbox("📂 Choose scenario (optional)",["Custom"]+list(templates.keys()))
    if template_name!="Custom":
        params=templates[template_name]
        troop=params['Troop_Count']
        terrain=params['Terrain']
        weather=params['Weather']
    else:
        troop=st.number_input("🧑‍✈️ Troop Count",10,5000,120,10)
        terrain=st.selectbox("⛰ Terrain",["Mountain","Desert","Forest","Plain"])
        weather=st.selectbox("🌦 Weather",["Cold","Hot","Moderate"])
    st.markdown("---")
    lang=st.radio("Language / भाषा",["English","हिन्दी"],horizontal=True)
    dark=st.checkbox("🌙 Dark Mode")
    st.markdown("---")
    predict=st.button("🔮 Predict Supplies",use_container_width=True)

# ---- Language helper ----
def tr(en,hi):
    return hi if lang=="हिन्दी" else en

# ---- Dark mode toggle ----
if dark:
    st.markdown("<style>body{background:#1e1e1e;color:#eee;} .metric h4{color:#ccc;} .metric h2{color:#fff;}</style>",unsafe_allow_html=True)

# ---- Load model ----
model=joblib.load(os.path.join('code','model.joblib'))

# ---- Prediction ----
if predict:
    X=pd.DataFrame({"Troop_Count":[troop],"Terrain":[terrain],"Weather":[weather]})
    fuel,food,meds,spare=model.predict(X)[0]
    cols=st.columns(4,gap="small")
    for c,label,val,unit,colr in [
        (cols[0],tr("Fuel","ईंधन"),fuel,"L",pb_cols[0]),
        (cols[1],tr("Food","खाद्य"),food,"Kg",pb_cols[1]),
        (cols[2],tr("Medicines","दवाएं"),meds,"Units",pb_cols[2]),
        (cols[3],tr("Spare Parts","स्पेयर पार्ट्स"),spare,"",pb_cols[3])]:
        with c:
            st.markdown(f"<div class='metric'><h4>{label}</h4><h2 style='color:{colr};'>{int(val):,} {unit}</h2></div>",unsafe_allow_html=True)

    # dummy last year
    np.random.seed(2)
    last_vals=[fuel*np.random.uniform(0.9,1.1),
               food*np.random.uniform(0.9,1.1),
               meds*np.random.uniform(0.9,1.1),
               spare*np.random.uniform(0.9,1.1)]
    bar_df=pd.DataFrame({"Supply":["Fuel","Food","Medicines","Spare Parts"]*2,
                         "Year":["Predicted"]*4+["Last Year"]*4,
                         "Quantity":[fuel,food,meds,spare]+last_vals})
    st.markdown(tr("### 📊 Predicted vs Last Year","### 📊 वर्तमान बनाम पिछला वर्ष"))
    st.plotly_chart(px.bar(bar_df,x="Supply",y="Quantity",color="Year",barmode="group",text_auto=".0f"),use_container_width=True)

    # cost savings
    fuel_price=96; food_price=150; med_price=50; spare_price=500
    saved=(last_vals[0]-fuel)*fuel_price
    st.success(f"{tr('Estimated Fuel Cost Saved','ईंधन लागत बचत अनुमानित')}: ₹{saved:,.0f}")

    # trend chart
    st.markdown(tr("### ⏱ 30‑Day Trend","### ⏱ 30‑दिन रुझान"))
    days=pd.date_range(end=datetime.today(),periods=30).strftime('%Y-%m-%d')
    trend=pd.DataFrame({"Date":np.tile(days,4),
                        "Quantity":np.concatenate([np.linspace(float(last_vals[i])*0.9,float(v),30) for i,v in enumerate([fuel,food,meds,spare])]),
                        "Supply":np.repeat(["Fuel","Food","Medicines","Spare Parts"],30)})
    st.plotly_chart(px.line(trend,x="Date",y="Quantity",color="Supply",template="army"),use_container_width=True)
else:
    st.info(tr("Enter mission details and click Predict.","मिशन विवरण भरें और भविष्यवाणी बटन दबाएँ।"))
