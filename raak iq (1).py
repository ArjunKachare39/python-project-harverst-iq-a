import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Harvest IQ", layout="wide", page_icon="🌿")

# Top Navbar/Header
st.markdown("### 🌿 Harvest IQ | Crop & Fertilizer Recommendation Engine")
st.divider()

# Category labels and icons
CATEGORY_ICONS = {
    "Food Crop": "🌾", 
    "Cash Crop": "💰", 
    "Spices and Plantation": "🌶️", 
    "Horticultural Crop": "🍎", 
    "Fodder Crop": "🐄"
}

# --- Database: Indian Crops & Environmental/Nutrient Requirements ---
# Ranges format: [min, max] for climate. Single integer for N, P, K (kg/ha optimal dose).
crops_db = {
    # FOOD CROPS
    "Rice (Paddy)": {"type": "Food Crop", "pH": [5.0, 6.5], "moisture": [60, 100], "temp": [20, 35], "humidity": [60, 90], "rain": [1000, 3000], "N": 100, "P": 50, "K": 50},
    "Wheat": {"type": "Food Crop", "pH": [6.0, 7.5], "moisture": [40, 60], "temp": [10, 25], "humidity": [40, 60], "rain": [450, 850], "N": 120, "P": 60, "K": 40},
    "Maize": {"type": "Food Crop", "pH": [5.5, 7.5], "moisture": [50, 70], "temp": [18, 27], "humidity": [50, 70], "rain": [500, 1000], "N": 120, "P": 60, "K": 40},
    "Jowar (Sorghum)": {"type": "Food Crop", "pH": [6.0, 7.5], "moisture": [30, 50], "temp": [25, 32], "humidity": [40, 60], "rain": [400, 750], "N": 80, "P": 40, "K": 40},
    "Bajra (Pearl Millet)": {"type": "Food Crop", "pH": [5.5, 7.5], "moisture": [20, 40], "temp": [25, 35], "humidity": [30, 50], "rain": [250, 600], "N": 60, "P": 30, "K": 30},
    "Ragi (Finger Millet)": {"type": "Food Crop", "pH": [5.0, 8.0], "moisture": [30, 50], "temp": [20, 30], "humidity": [40, 60], "rain": [500, 1000], "N": 60, "P": 30, "K": 30},
    "Barley": {"type": "Food Crop", "pH": [6.0, 8.0], "moisture": [30, 50], "temp": [12, 25], "humidity": [40, 60], "rain": [350, 550], "N": 60, "P": 30, "K": 20},
    "Chickpea (Gram)": {"type": "Food Crop", "pH": [6.0, 7.5], "moisture": [30, 50], "temp": [20, 30], "humidity": [30, 50], "rain": [600, 900], "N": 20, "P": 40, "K": 20},
    "Pigeon Pea (Tur)": {"type": "Food Crop", "pH": [6.5, 7.5], "moisture": [40, 60], "temp": [25, 35], "humidity": [40, 60], "rain": [600, 1000], "N": 20, "P": 50, "K": 20},
    "Green Gram (Moong)": {"type": "Food Crop", "pH": [6.0, 7.5], "moisture": [40, 60], "temp": [25, 35], "humidity": [40, 60], "rain": [600, 800], "N": 20, "P": 40, "K": 20},
    "Black Gram (Urad)": {"type": "Food Crop", "pH": [5.5, 7.5], "moisture": [40, 60], "temp": [25, 35], "humidity": [40, 60], "rain": [600, 800], "N": 20, "P": 40, "K": 20},
    "Lentils": {"type": "Food Crop", "pH": [6.0, 7.0], "moisture": [30, 50], "temp": [15, 25], "humidity": [40, 60], "rain": [400, 600], "N": 20, "P": 40, "K": 20},
    "Potato": {"type": "Food Crop", "pH": [5.0, 6.5], "moisture": [50, 70], "temp": [15, 25], "humidity": [50, 70], "rain": [500, 1200], "N": 120, "P": 80, "K": 100},
    "Sweet Potato": {"type": "Food Crop", "pH": [5.5, 6.5], "moisture": [50, 70], "temp": [21, 29], "humidity": [60, 80], "rain": [750, 1500], "N": 75, "P": 50, "K": 75},

    # CASH CROPS
    "Cotton": {"type": "Cash Crop", "pH": [6.0, 8.0], "moisture": [40, 60], "temp": [21, 30], "humidity": [50, 70], "rain": [500, 1000], "N": 120, "P": 60, "K": 60},
    "Sugarcane": {"type": "Cash Crop", "pH": [6.5, 7.5], "moisture": [70, 90], "temp": [20, 35], "humidity": [60, 80], "rain": [1500, 2500], "N": 150, "P": 80, "K": 80},
    "Groundnut": {"type": "Cash Crop", "pH": [6.0, 6.5], "moisture": [40, 60], "temp": [25, 30], "humidity": [50, 70], "rain": [500, 1000], "N": 25, "P": 50, "K": 50},
    "Soybean": {"type": "Cash Crop", "pH": [6.0, 7.0], "moisture": [50, 70], "temp": [20, 30], "humidity": [50, 70], "rain": [600, 1000], "N": 30, "P": 60, "K": 40},
    "Mustard": {"type": "Cash Crop", "pH": [6.0, 7.5], "moisture": [30, 50], "temp": [10, 25], "humidity": [40, 60], "rain": [300, 500], "N": 80, "P": 40, "K": 40},
    "Sunflower": {"type": "Cash Crop", "pH": [6.0, 7.5], "moisture": [40, 60], "temp": [20, 30], "humidity": [50, 70], "rain": [500, 800], "N": 60, "P": 40, "K": 40},
    "Sesame": {"type": "Cash Crop", "pH": [5.5, 8.0], "moisture": [30, 50], "temp": [25, 35], "humidity": [40, 60], "rain": [400, 600], "N": 40, "P": 20, "K": 20},
    "Tobacco": {"type": "Cash Crop", "pH": [5.5, 6.5], "moisture": [50, 70], "temp": [20, 30], "humidity": [60, 80], "rain": [500, 1200], "N": 90, "P": 50, "K": 60},
    "Jute": {"type": "Cash Crop", "pH": [6.0, 7.5], "moisture": [70, 90], "temp": [24, 35], "humidity": [70, 90], "rain": [1500, 2000], "N": 80, "P": 40, "K": 40},
    "Tea": {"type": "Cash Crop", "pH": [4.5, 5.5], "moisture": [60, 80], "temp": [20, 30], "humidity": [70, 90], "rain": [1500, 3000], "N": 100, "P": 50, "K": 50},
    "Coffee": {"type": "Cash Crop", "pH": [5.0, 6.0], "moisture": [60, 80], "temp": [15, 28], "humidity": [70, 90], "rain": [1500, 2500], "N": 100, "P": 50, "K": 50},
    "Rubber": {"type": "Cash Crop", "pH": [4.5, 6.0], "moisture": [70, 90], "temp": [25, 35], "humidity": [80, 100], "rain": [2000, 4000], "N": 75, "P": 50, "K": 50},

    # SPICES & PLANTATION
    "Turmeric": {"type": "Spices and Plantation", "pH": [5.5, 7.5], "moisture": [60, 80], "temp": [20, 30], "humidity": [60, 80], "rain": [1500, 2500], "N": 120, "P": 60, "K": 90},
    "Ginger": {"type": "Spices and Plantation", "pH": [5.5, 6.5], "moisture": [60, 80], "temp": [20, 30], "humidity": [60, 80], "rain": [1500, 2500], "N": 100, "P": 50, "K": 50},
    "Chilli": {"type": "Spices and Plantation", "pH": [6.0, 7.0], "moisture": [40, 60], "temp": [20, 30], "humidity": [50, 70], "rain": [600, 1200], "N": 100, "P": 50, "K": 50},
    "Black Pepper": {"type": "Spices and Plantation", "pH": [5.5, 6.5], "moisture": [60, 80], "temp": [20, 30], "humidity": [70, 90], "rain": [2000, 3000], "N": 100, "P": 40, "K": 140},
    "Cardamom": {"type": "Spices and Plantation", "pH": [5.5, 6.5], "moisture": [70, 90], "temp": [10, 25], "humidity": [70, 90], "rain": [1500, 3500], "N": 75, "P": 75, "K": 150},
    "Coriander": {"type": "Spices and Plantation", "pH": [6.0, 8.0], "moisture": [40, 60], "temp": [20, 25], "humidity": [40, 60], "rain": [500, 700], "N": 30, "P": 30, "K": 20},
    "Cumin": {"type": "Spices and Plantation", "pH": [6.5, 8.0], "moisture": [30, 50], "temp": [25, 30], "humidity": [40, 60], "rain": [300, 500], "N": 30, "P": 20, "K": 20},
    "Coconut": {"type": "Spices and Plantation", "pH": [5.2, 8.0], "moisture": [60, 80], "temp": [27, 32], "humidity": [70, 90], "rain": [1300, 2300], "N": 150, "P": 50, "K": 150},
    "Arecanut": {"type": "Spices and Plantation", "pH": [5.0, 8.0], "moisture": [60, 80], "temp": [14, 36], "humidity": [70, 90], "rain": [1500, 4000], "N": 150, "P": 50, "K": 150},
    "Cashew": {"type": "Spices and Plantation", "pH": [5.0, 6.5], "moisture": [40, 60], "temp": [20, 35], "humidity": [60, 80], "rain": [1000, 3000], "N": 100, "P": 40, "K": 60},

    # HORTICULTURAL CROPS
    "Mango": {"type": "Horticultural Crop", "pH": [5.5, 7.5], "moisture": [40, 60], "temp": [24, 30], "humidity": [40, 60], "rain": [750, 2500], "N": 100, "P": 50, "K": 100},
    "Banana": {"type": "Horticultural Crop", "pH": [6.5, 7.5], "moisture": [70, 90], "temp": [15, 35], "humidity": [70, 90], "rain": [1500, 2500], "N": 200, "P": 100, "K": 200},
    "Grapes": {"type": "Horticultural Crop", "pH": [6.5, 7.5], "moisture": [40, 60], "temp": [15, 40], "humidity": [40, 60], "rain": [500, 900], "N": 150, "P": 80, "K": 150},
    "Pomegranate": {"type": "Horticultural Crop", "pH": [6.5, 7.5], "moisture": [30, 50], "temp": [25, 35], "humidity": [30, 50], "rain": [500, 800], "N": 100, "P": 50, "K": 50},
    "Papaya": {"type": "Horticultural Crop", "pH": [6.0, 7.0], "moisture": [60, 80], "temp": [22, 26], "humidity": [60, 80], "rain": [1000, 1500], "N": 150, "P": 150, "K": 150},
    "Guava": {"type": "Horticultural Crop", "pH": [4.5, 8.2], "moisture": [40, 60], "temp": [23, 28], "humidity": [40, 60], "rain": [1000, 2000], "N": 100, "P": 50, "K": 100},
    "Orange": {"type": "Horticultural Crop", "pH": [5.5, 7.5], "moisture": [50, 70], "temp": [15, 30], "humidity": [50, 70], "rain": [1000, 2000], "N": 150, "P": 50, "K": 100},
    "Apple": {"type": "Horticultural Crop", "pH": [5.5, 6.5], "moisture": [50, 70], "temp": [21, 24], "humidity": [50, 70], "rain": [1000, 1250], "N": 100, "P": 50, "K": 100},
    "Onion": {"type": "Horticultural Crop", "pH": [6.0, 7.5], "moisture": [50, 70], "temp": [13, 24], "humidity": [60, 70], "rain": [500, 750], "N": 100, "P": 50, "K": 50},
    "Tomato": {"type": "Horticultural Crop", "pH": [6.0, 7.0], "moisture": [50, 70], "temp": [21, 24], "humidity": [50, 70], "rain": [600, 1000], "N": 120, "P": 60, "K": 60},
    "Brinjal": {"type": "Horticultural Crop", "pH": [5.5, 6.5], "moisture": [50, 70], "temp": [21, 30], "humidity": [50, 70], "rain": [500, 1000], "N": 100, "P": 50, "K": 50},
    "Okra": {"type": "Horticultural Crop", "pH": [6.0, 6.8], "moisture": [50, 70], "temp": [24, 30], "humidity": [60, 80], "rain": [1000, 1500], "N": 100, "P": 50, "K": 50},

    # FODDER CROPS
    "Berseem": {"type": "Fodder Crop", "pH": [6.5, 8.0], "moisture": [60, 80], "temp": [15, 25], "humidity": [50, 70], "rain": [500, 800], "N": 25, "P": 60, "K": 40},
    "Lucerne": {"type": "Fodder Crop", "pH": [6.5, 7.5], "moisture": [50, 70], "temp": [15, 25], "humidity": [40, 60], "rain": [500, 700], "N": 25, "P": 60, "K": 40},
    "Napier Grass": {"type": "Fodder Crop", "pH": [5.0, 8.0], "moisture": [60, 80], "temp": [25, 35], "humidity": [50, 70], "rain": [1000, 2000], "N": 150, "P": 50, "K": 50},
    "Fodder Maize": {"type": "Fodder Crop", "pH": [5.5, 7.5], "moisture": [50, 70], "temp": [20, 30], "humidity": [50, 70], "rain": [500, 1000], "N": 100, "P": 50, "K": 50},
    "Fodder Sorghum": {"type": "Fodder Crop", "pH": [6.0, 7.5], "moisture": [30, 50], "temp": [25, 32], "humidity": [40, 60], "rain": [400, 750], "N": 80, "P": 40, "K": 40},
    "Oats": {"type": "Fodder Crop", "pH": [5.5, 7.0], "moisture": [50, 70], "temp": [15, 25], "humidity": [50, 70], "rain": [400, 600], "N": 80, "P": 40, "K": 40},
}

# --- Core Algorithm ---
def calculate_range_score(value, optimal_range, tolerance):
    """Calculates 0-100 score for environmental parameters using a range."""
    min_val, max_val = optimal_range
    if min_val <= value <= max_val:
        return 100.0, "Optimal"
    
    if value < min_val:
        deviation = min_val - value
        status = "Too Low"
    else:
        deviation = value - max_val
        status = "Too High"
        
    score = max(0.0, 100 - (deviation / tolerance) * 100)
    return score, status

def calculate_nutrient_score(input_val, target_val, tolerance):
    """Calculates 0-100 score for NPK based on target dose."""
    if input_val >= target_val:
        return 100.0, "Optimal/Surplus"
    
    deviation = target_val - input_val
    score = max(0.0, 100 - (deviation / tolerance) * 100)
    return score, "Deficient"

def evaluate_crops(inputs):
    """Evaluates all crops against all 8 parameters (5 Climate/Soil + 3 NPK)"""
    
    range_tolerances = {
        "pH": 2.0,            # 2 pH units off = 0 score
        "moisture": 30.0,     # 30% off = 0 score
        "temp": 15.0,         # 15 degrees off = 0 score
        "humidity": 30.0,     # 30% off = 0 score
        "rain": 800.0         # 800mm off = 0 score
    }
    
    nutrient_tolerances = {
        "N": 60.0,            # 60 kg/ha deficient = 0 score
        "P": 40.0,
        "K": 40.0
    }
    
    results = []
    
    for crop, data in crops_db.items():
        scores = {}
        statuses = {}
        
        # 1. Evaluate 5 Environmental Parameters
        for param in ["pH", "moisture", "temp", "humidity", "rain"]:
            s, status = calculate_range_score(inputs[param], data[param], range_tolerances[param])
            scores[param] = s
            statuses[param] = status
            
        # 2. Evaluate 3 Nutrient Parameters
        for param in ["N", "P", "K"]:
            s, status = calculate_nutrient_score(inputs[param], data[param], nutrient_tolerances[param])
            scores[param] = s
            statuses[param] = status
            
        # 3. Combined Score (Average of all 8 parameters)
        total_score = sum(scores.values()) / 8.0
        
        # Identify the primary limiting factor (lowest scoring parameter)
        limiting_param = min(scores, key=scores.get)
        limiting_score = scores[limiting_param]
        
        results.append({
            "Crop": crop,
            "Type": data["type"],
            "Score": round(total_score, 1),
            "Scores": scores,
            "Statuses": statuses,
            "Limiting_Param": limiting_param if limiting_score < 100 else "None",
            "Data": data
        })
        
    return sorted(results, key=lambda x: x["Score"], reverse=True)


# --- UI Layout ---
left_col, right_col = st.columns([1, 2.5], gap="large")

with left_col:
    st.subheader("🪴 Input Parameters")
    
    with st.container(border=True):
        st.markdown("#### 01. SOIL NUTRIENTS (KG/HA)")
        n = st.slider("Nitrogen (N)", 0, 250, 60)
        p = st.slider("Phosphorus (P)", 0, 150, 45)
        k = st.slider("Potassium (K)", 0, 200, 40)
        
    with st.container(border=True):
        st.markdown("#### 02. SOIL PARAMETERS")
        ph = st.slider("Soil pH", 3.5, 10.0, 6.5, 0.1)
        moisture = st.slider("Soil Moisture (%)", 0, 100, 50)
        
    with st.container(border=True):
        st.markdown("#### 03. CLIMATE PARAMETERS")
        temp = st.slider("Avg Temperature (°C)", 0, 50, 26)
        humidity = st.slider("Relative Humidity (%)", 0, 100, 60)
        rain = st.slider("Annual Rainfall (mm)", 0, 4000, 800)

    st.write("") # Spacing
    st.button("🪄 Calculate Recommendation", type="primary", use_container_width=True)

    inputs = {"pH": ph, "moisture": moisture, "temp": temp, "humidity": humidity, "rain": rain, "N": n, "P": p, "K": k}

with right_col:
    # Run Algorithm
    evaluated_crops = evaluate_crops(inputs)
    top_crop = evaluated_crops[0]
    
    # --- TOP KPI CARDS ---
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        with st.container(border=True):
            st.metric(label="TOP RECOMMENDATION", value=top_crop["Crop"], delta=f"{top_crop['Score']}% Overall Match")

    with kpi2:
        with st.container(border=True):
            if top_crop["Limiting_Param"] == "None":
                st.metric(label="LIMITING FACTOR", value="Optimal", delta="All conditions met", delta_color="normal")
            else:
                lim_p = top_crop["Limiting_Param"]
                status = top_crop["Statuses"][lim_p]
                
                param_names = {"pH": "Soil pH", "moisture": "Moisture", "temp": "Temperature", "humidity": "Humidity", "rain": "Rainfall", "N": "Nitrogen", "P": "Phosphorus", "K": "Potassium"}
                param_name = param_names[lim_p]
                
                st.metric(label="LIMITING FACTOR", value=param_name, delta=status, delta_color="inverse")

    with kpi3:
        with st.container(border=True):
            perfect_params = sum(1 for s in top_crop["Scores"].values() if s == 100)
            st.metric(label="PARAMETER MATCH", value=f"{perfect_params} / 8", delta="Metrics in ideal range")

    st.write("") 

    # --- TABBED INTERFACE ---
    tab1, tab2, tab3, tab4 = st.tabs(["📑 Ranked Recommendations", "📊 Parameter Breakdown", "🧪 Fertilizer Action Plan", "💡 Suitability Insights"])

    with tab1:
        st.caption("TOP 6 HIGHLY COMPATIBLE CROPS")
        grid_cols = st.columns(2)
        for i, crop_data in enumerate(evaluated_crops[:6]): 
            col = grid_cols[i % 2]
            with col:
                with st.container(border=True):
                    card_col1, card_col2 = st.columns([3, 1])
                    card_col1.markdown(f"**{crop_data['Crop']}**")
                    card_col2.success(f"{crop_data['Score']}%")

                    icon = CATEGORY_ICONS[crop_data["Type"]]
                    st.caption(f"{icon} {crop_data['Type']} | Ideal NPK: {crop_data['Data']['N']}-{crop_data['Data']['P']}-{crop_data['Data']['K']}")
                    
                    issues = [k for k, v in crop_data["Scores"].items() if v < 100]
                    if not issues:
                        st.write("*Perfectly suited for these conditions.*")
                    else:
                        st.write(f"*Sub-optimal metrics: {', '.join(issues).title()}*")
                        
                    st.progress(crop_data["Score"] / 100)

    with tab2:
        st.caption(f"8-PARAMETER BREAKDOWN: {top_crop['Crop'].upper()}")
        
        df_breakdown = pd.DataFrame({
            "Parameter": ["Soil pH", "Moisture (%)", "Temp (°C)", "Humidity (%)", "Rainfall (mm)", "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
            "Your Input": [ph, moisture, temp, humidity, rain, n, p, k],
            "Optimal Range / Target": [
                f"{top_crop['Data']['pH'][0]} - {top_crop['Data']['pH'][1]}",
                f"{top_crop['Data']['moisture'][0]} - {top_crop['Data']['moisture'][1]}",
                f"{top_crop['Data']['temp'][0]} - {top_crop['Data']['temp'][1]}",
                f"{top_crop['Data']['humidity'][0]} - {top_crop['Data']['humidity'][1]}",
                f"{top_crop['Data']['rain'][0]} - {top_crop['Data']['rain'][1]}",
                f"{top_crop['Data']['N']} kg/ha",
                f"{top_crop['Data']['P']} kg/ha",
                f"{top_crop['Data']['K']} kg/ha"
            ],
            "Parameter Score": [f"{round(top_crop['Scores'][p])}%" for p in ["pH", "moisture", "temp", "humidity", "rain", "N", "P", "K"]],
            "Status": [top_crop["Statuses"][p] for p in ["pH", "moisture", "temp", "humidity", "rain", "N", "P", "K"]]
        })
        st.table(df_breakdown)

    with tab3:
        st.caption(f"REQUIRED SUPPLEMENTATION (KG/HA) FOR {top_crop['Crop'].upper()}")
        
        req = top_crop["Data"]
        urea = max(0, round((req["N"] - n) / 0.46))
        dap = max(0, round((req["P"] - p) / 0.46))
        mop = max(0, round((req["K"] - k) / 0.60))

        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            with st.container(border=True):
                st.metric("Urea (Nitrogen Source)", f"{urea} kg", delta=f"{max(0, req['N'] - n)} kg N deficit" if urea > 0 else "Optimal N", delta_color="inverse" if urea > 0 else "normal")
        with f_col2:
            with st.container(border=True):
                st.metric("DAP (Phosphorus Source)", f"{dap} kg", delta=f"{max(0, req['P'] - p)} kg P deficit" if dap > 0 else "Optimal P", delta_color="inverse" if dap > 0 else "normal")
        with f_col3:
            with st.container(border=True):
                st.metric("MOP (Potassium Source)", f"{mop} kg", delta=f"{max(0, req['K'] - k)} kg K deficit" if mop > 0 else "Optimal K", delta_color="inverse" if mop > 0 else "normal")
                
        st.write("")
        st.caption("CURRENT VS TARGET NUTRIENTS")
        df_npk = pd.DataFrame({
            "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
            "Current Base Level": [n, p, k],
            "Required Total": [req["N"], req["P"], req["K"]]
        }).set_index("Nutrient")
        st.bar_chart(df_npk, color=["#1f77b4", "#2ca02c"])

    with tab4:
        st.caption("WHY THIS CROP WAS SELECTED")
        st.markdown(f"**{top_crop['Crop']}** was chosen as the top recommendation because it achieved the highest combined suitability score of **{top_crop['Score']}%** across both environmental constraints and existing soil nutrients.")
        
        good_params = [k for k, v in top_crop["Scores"].items() if v == 100]
        bad_params = [(k, top_crop["Statuses"][k]) for k, v in top_crop["Scores"].items() if v < 100]
        
        if good_params:
            st.markdown("✅ **Favorable Conditions:** " + ", ".join(good_params).title() + " inputs perfectly match this crop's biological requirements.")
        if bad_params:
            st.markdown("⚠️ **Challenges to Manage:**")
            for bp, status in bad_params:
                if bp in ["N", "P", "K"]:
                    st.markdown(f"- **{bp.upper()} Nutrient**: Currently *{status.lower()}*. Address this via the Fertilizer Action Plan.")
                else:
                    st.markdown(f"- **{bp.title()}**: Currently *{status.lower()}*. Consider agricultural interventions (e.g., irrigation, drainage, or soil amendments) to mitigate this environmental mismatch.")

# --- BOTTOM SECTION: CROP CATEGORIES ---
st.divider()
st.subheader("🗂️ Explore Full Indian Crop Database")

category_filter = st.radio(
    "Filter by category",
    ["All"] + list(CATEGORY_ICONS.keys()),
    horizontal=True,
    label_visibility="collapsed",
)

db_list = []
for c in evaluated_crops:
    db_list.append({
        "Crop": c["Crop"],
        "Category": f"{CATEGORY_ICONS[c['Type']]} {c['Type']}",
        "8-Param Match Score": c["Score"],
        "Target NPK": f"{c['Data']['N']}-{c['Data']['P']}-{c['Data']['K']}",
        "pH Range": f"{c['Data']['pH'][0]} - {c['Data']['pH'][1]}",
        "Temp Range": f"{c['Data']['temp'][0]} - {c['Data']['temp'][1]}°C",
        "Rain Range": f"{c['Data']['rain'][0]} - {c['Data']['rain'][1]}mm",
    })

category_df = pd.DataFrame(db_list)

if category_filter != "All":
    category_df = category_df[category_df["Category"].str.contains(category_filter)]

st.dataframe(
    category_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "8-Param Match Score": st.column_config.ProgressColumn("Suitability", min_value=0, max_value=100, format="%d%%"),
    },
)