import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---- Custom CSS Styles and Logo ----
plant_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Plant_leaf_icon.svg/512px-Plant_leaf_icon.svg.png"

st.markdown(
    f"""
    <style>
    body {{
        background: linear-gradient(120deg, #0d1117 20%, #168039 45%, #0351a2 100%) !important;
        color: #E1E8ED;
    }}
    .stApp {{
        background: linear-gradient(120deg, #0d1117 20%, #168039 45%, #0351a2 100%) !important;
    }}
    .plant-logo {{
        position: fixed;
        top: 18px;
        right: 18px;
        z-index: 100;
    }}
    .stDataFrame, .stTable {{
        background-color: rgba(20,20,35,0.9) !important;
    }}
    h1, h2, h3, h4, h5, h6, label, div, span {{
        color: #E1E8ED !important;
    }}
    .element-container {{
        background: none !important;
    }}
    .panel {{
        background: #191c24;
        border-radius: 12px;
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 10px;
        box-shadow: 0 1px 6px 0 rgba(0,0,0,0.22);
        color: #f2f2f2;
    }}
    .main-title {{
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #8A2BE2, #DA70D6, #9370DB, #4B0082);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        padding: 10px;
    }}
    .subtitle {{
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: #B0B8C4 !important;
    }}
    .chart-container {{
        background: #191c24;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }}
    </style>
    <img src="{plant_logo_url}" class="plant-logo" width="68" title="Green Plant Logo"/>
    """,
    unsafe_allow_html=True
)

# ---- Centered Main Title ----
st.markdown('<div class="main-title">🌱 GREEN METER APP</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">CO₂ Emissions Calculator for Logistics</div>', unsafe_allow_html=True)

# ---- Sidebar Inputs ----
with st.sidebar:
    st.header("Inputs · Activity Data")
    cars_km = st.number_input("Cars distance (km/year)", min_value=0.0, value=1.0)
    trucks_km = st.number_input("Trucks distance (km/year)", min_value=0.0, value=0.0)
    buses_km = st.number_input("Buses distance (km/year)", min_value=0.0, value=0.0)
    forklifts_hr = st.number_input("Forklifts operating time (hrs/year)", min_value=0.0, value=0.0)
    planes_hr = st.number_input("Cargo Planes flight time (hrs/year)", min_value=0.0, value=0.0)
    heating_kwh = st.number_input("Heating (thermal energy kWh-th/year)", min_value=0.0, value=0.0)
    lighting_kwh = st.number_input("Office Lighting (electricity kWh/year)", min_value=0.0, value=0.0)
    cooling_kwh = st.number_input("Cooling (A/C electricity kWh/year)", min_value=0.0, value=0.0)
    computing_kwh = st.number_input("Computing (IT electricity kWh/year)", min_value=0.0, value=0.0)
    st.subheader("Subcontractors (tons CO₂/year)")
    sub1 = st.number_input("Subcontractor 1", min_value=0.0, value=0.0)
    sub2 = st.number_input("Subcontractor 2", min_value=0.0, value=0.0)
    sub3 = st.number_input("Subcontractor 3", min_value=0.0, value=0.0)

    st.header("Adjustments · Sliders")
    ev_share = st.slider("EV Share for Cars (%)", min_value=0, max_value=100, value=0)
    km_reduction = st.slider("KM Reduction for Cars (%)", min_value=0, max_value=100, value=0)
    plane_load_factor = st.slider("Plane Load Factor (%)", min_value=0, max_value=100, value=0)

# ---- Main Content ----
st.write("Compare total and category-wise CO₂ emissions for your logistics company. Adjust EV share, travel reduction, and plane load factor to see instant effect!")

# ---- Emissions Calculation Factors ----
EF_cars = 0.18
EF_trucks = 0.90
EF_buses = 1.10
EF_forklifts = 4.0
EF_planes = 9000
EF_lighting = 0.42
EF_heating = 0.20
EF_cooling = 0.42
EF_computing = 0.42

cars_baseline = (cars_km * EF_cars) / 1000
trucks_baseline = (trucks_km * EF_trucks) / 1000
buses_baseline = (buses_km * EF_buses) / 1000
forklifts_baseline = (forklifts_hr * EF_forklifts) / 1000
planes_baseline = (planes_hr * EF_planes) / 1000
lighting_baseline = (lighting_kwh * EF_lighting) / 1000
heating_baseline = (heating_kwh * EF_heating) / 1000
cooling_baseline = (cooling_kwh * EF_cooling) / 1000
computing_baseline = (computing_kwh * EF_computing) / 1000
subcontractors_baseline = sub1 + sub2 + sub3

total_baseline = (cars_baseline + trucks_baseline + buses_baseline +
                  forklifts_baseline + planes_baseline + lighting_baseline +
                  heating_baseline + cooling_baseline + computing_baseline +
                  subcontractors_baseline)

cars_optimized = ((cars_km * EF_cars)*(1 - 0.7 * ev_share/100)*(1 - km_reduction/100))/1000
trucks_optimized = trucks_baseline
buses_optimized = buses_baseline
forklifts_optimized = forklifts_baseline
planes_optimized = ((planes_hr * EF_planes)*(plane_load_factor/100))/1000
lighting_optimized = lighting_baseline
heating_optimized = heating_baseline
cooling_optimized = cooling_baseline
computing_optimized = computing_baseline
subcontractors_optimized = subcontractors_baseline

total_optimized = (cars_optimized + trucks_optimized + buses_optimized +
                   forklifts_optimized + planes_optimized + lighting_optimized +
                   heating_optimized + cooling_optimized + computing_optimized +
                   subcontractors_optimized)

reduction = total_baseline - total_optimized
reduction_pct = (reduction / total_baseline) * 100 if total_baseline else 0

categories = ['Cars', 'Trucks', 'Buses', 'Forklifts', 'Cargo Planes',
              'Office Lighting', 'Heating', 'Cooling (A/C)', 'Computing (IT)', 'Subcontractors']

baseline_vals = [cars_baseline, trucks_baseline, buses_baseline, forklifts_baseline,
                 planes_baseline, lighting_baseline, heating_baseline, cooling_baseline,
                 computing_baseline, subcontractors_baseline]

optimized_vals = [cars_optimized, trucks_optimized, buses_optimized, forklifts_optimized,
                  planes_optimized, lighting_optimized, heating_optimized, cooling_optimized,
                  computing_optimized, subcontractors_optimized]

# ---- KPI/Results Panel ----
st.markdown(f"""
    <div style="display:flex; gap:30px;">
        <div class="panel">
            <h4>Baseline Total</h4>
            <span style="font-size:28px; font-weight:bold;">{total_baseline:.1f} tons CO₂</span>
        </div>
        <div class="panel">
            <h4>Optimized Total</h4>
            <span style="font-size:28px; font-weight:bold;">{total_optimized:.1f} tons CO₂</span>
        </div>
    </div>
""", unsafe_allow_html=True)
st.info(f"Total Reduction: {reduction:.1f} tons CO₂/year ({reduction_pct:.1f}%)")

# ---- Results Table ----
results = {
    'Category': categories,
    'Baseline (t CO₂)': np.round(baseline_vals,2),
    'Optimized (t CO₂)': np.round(optimized_vals,2),
    'Reduction (t CO₂)': np.round(np.array(baseline_vals)-np.array(optimized_vals),2)
}
st.dataframe(results)

# ---- Side-by-Side Charts ----
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)  # Equal columns for both charts

with col1:
    st.subheader("Emission Share by Category (Pie - Optimized)")

    fig, ax = plt.subplots(figsize=(16, 20))  # Bigger pie chart
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFD700', '#FF69B4',
              '#C9A0DC', '#FFA07A', '#20B2AA', '#F0E68C', '#D3D3D3']
    wedges, texts, autotexts = ax.pie(
        optimized_vals,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize':  40}  # Slightly bigger text
    )
    ax.axis('equal')
    # Improved legend placement
    ax.legend(wedges, categories, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=40)
    st.pyplot(fig)

with col2:
    st.subheader("Total Emissions · Baseline vs Optimized")
    fig2, ax2 = plt.subplots(figsize=(20, 25))  # Same size as pie chart
    bars = ax2.bar(['Baseline','Optimized'], [total_baseline,total_optimized], 
                   color=['#FF6B6B','#4ECDC4'], width=0.6)
    ax2.set_ylabel('Total Emissions (tons CO₂/year)', fontweight='bold', fontsize=58)
    ax2.set_ylim(0, max(total_baseline,total_optimized)*1.2)
    
    # Better bar labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.tick_params(axis='both', which='major', labelsize=50)
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(total_baseline,total_optimized)*0.05, 
                f"{height:.1f} t", 
                ha='center', va='bottom', fontweight='bold', fontsize=58, color='#E1E8ED')
    
    # Add value on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height/2, 
                f"{height:.1f}", 
                ha='center', va='center', fontweight='bold', fontsize=58, color='white')
    
    ax2.grid(axis='y', alpha=0.3)
    # Remove top and right spines for cleaner look
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    st.pyplot(fig2)

st.markdown('</div>', unsafe_allow_html=True)

st.caption("Breakdown, charts, sliders, and layout match the dashboard style from your screenshot. Adjust inputs for instant visualization!")