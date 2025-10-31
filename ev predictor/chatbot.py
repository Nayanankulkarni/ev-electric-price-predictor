import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="⚡ EV AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stunning CSS with animations and modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        animation: fadeIn 0.8s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid rgba(255,255,255,0.3);
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        animation: slideDown 0.8s ease;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .header-title {
        font-size: 3.5em;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: pulse 2s ease infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .header-subtitle {
        color: white;
        font-size: 1.3em;
        margin-top: 10px;
        font-weight: 300;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Chat messages with 3D effect */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2), 
                    0 1px 8px rgba(0,0,0,0.1) !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
        transform: translateZ(0);
        transition: all 0.3s ease !important;
        animation: messageSlide 0.5s ease;
    }
    
    @keyframes messageSlide {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .stChatMessage:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3) !important;
    }
    
    /* User message - gradient background */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Assistant message - white with gradient border */
    .stChatMessage[data-testid="assistant-message"] {
        background: white !important;
        border: 3px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2, #f093fb) 1;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Button styling with hover effects */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px 30px;
        font-size: 1.1em;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Input field styling */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 10px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid rgba(255,255,255,0.3);
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: fadeIn 1s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 0.9em;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
        margin-top: 5px;
    }
    
    /* Floating emoji animation */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Quick action cards */
    .quick-action {
        background: linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.15));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid rgba(255,255,255,0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        color: white;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .quick-action:hover {
        transform: translateX(10px);
        background: linear-gradient(135deg, rgba(255,255,255,0.4), rgba(255,255,255,0.25));
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: '...';
        animation: dots 1.5s steps(4, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60%, 100% { content: '...'; }
    }
    
    /* Stats badge */
    .stats-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 600;
        margin: 5px;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
        animation: fadeIn 0.8s ease;
    }
    
    /* Feature tags */
    .feature-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        color: white;
        padding: 5px 15px;
        border-radius: 15px;
        margin: 3px;
        font-size: 0.85em;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #f093fb);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data and models
@st.cache_resource
def load_models():
    try:
        with open('ev_price_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        return model, scaler, encoders
    except:
        return None, None, None

@st.cache_data
def load_data():
    df = pd.read_csv('ElectricCarData_Clean (1).csv')
    df.columns = df.columns.str.strip()
    df['Brand'] = df['Brand'].str.strip()
    df['Model'] = df['Model'].str.strip()
    df['FastCharge_KmH'] = pd.to_numeric(df['FastCharge_KmH'], errors='coerce')
    return df

df = load_data()
model, scaler, encoders = load_models()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_message = """
<div style='font-size: 1.2em; line-height: 1.8;'>
    <div style='font-size: 2em; margin-bottom: 15px;'>👋 Welcome to EV AI Assistant!</div>
    
    I'm your intelligent guide to the world of electric vehicles! Here's what I can do:
    
    <div style='margin: 20px 0;'>
        <span class='feature-tag'>🚗 Find Perfect EVs</span>
        <span class='feature-tag'>💰 Predict Prices</span>
        <span class='feature-tag'>📊 Compare Models</span>
        <span class='feature-tag'>❓ Answer Questions</span>
    </div>
    
    <div style='background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2)); 
                padding: 20px; border-radius: 15px; margin: 20px 0;'>
        <b>✨ Try asking:</b><br>
        • "Show me affordable EVs under €40,000"<br>
        • "What are the fastest Tesla models?"<br>
        • "Predict price for my custom EV"<br>
        • "Compare SUVs by range"
    </div>
    
    <div style='text-align: center; font-size: 1.5em; margin-top: 20px;'>
        What would you like to explore today? 🚀
    </div>
</div>
"""
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_message
    })

if "prediction_mode" not in st.session_state:
    st.session_state.prediction_mode = False
    st.session_state.prediction_step = 0
    st.session_state.prediction_data = {}

# Stunning Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">
            <span class="floating">🤖</span> EV AI Assistant <span class="floating">⚡</span>
        </div>
        <div class="header-subtitle">
            Your Intelligent Guide to Electric Vehicles
        </div>
        <div style="margin-top: 20px;">
            <span class="stats-badge">💡 Smart Predictions</span>
            <span class="stats-badge">🎯 Expert Insights</span>
            <span class="stats-badge">⚡ Instant Answers</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# AI Response Functions (keeping existing logic)
def get_ev_info(query):
    """Get information about EVs based on query"""
    query_lower = query.lower()
    
    # Brand queries
    if "brand" in query_lower or "brands" in query_lower:
        brands = df['Brand'].value_counts().head(10)
        response = """
<div style='background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #667eea;'>
    <h3 style='color: #667eea; margin-top: 0;'>🏢 Top EV Brands</h3>
"""
        for brand, count in brands.items():
            response += f"<div style='padding: 8px; margin: 5px 0; background: rgba(255,255,255,0.5); border-radius: 10px;'>• <b>{brand}</b>: {count} models</div>"
        response += "</div>"
        return response
    
    # Price queries
    if "cheap" in query_lower or "affordable" in query_lower or "budget" in query_lower:
        cheap_evs = df.nsmallest(5, 'PriceEuro')[['Brand', 'Model', 'PriceEuro', 'Range_Km']]
        response = """
<div style='background: linear-gradient(135deg, rgba(76,175,80,0.1), rgba(139,195,74,0.1)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #4caf50;'>
    <h3 style='color: #4caf50; margin-top: 0;'>💰 Most Affordable EVs</h3>
"""
        for _, row in cheap_evs.iterrows():
            response += f"""
<div style='padding: 15px; margin: 10px 0; background: rgba(255,255,255,0.7); border-radius: 12px; 
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
    <b style='color: #667eea; font-size: 1.2em;'>{row['Brand']} {row['Model']}</b><br>
    <span style='color: #4caf50; font-size: 1.3em; font-weight: 700;'>€{row['PriceEuro']:,.0f}</span> • 
    <span style='color: #666;'>{row['Range_Km']} km range</span>
</div>"""
        response += "</div>"
        return response
    
    if "expensive" in query_lower or "luxury" in query_lower or "premium" in query_lower:
        expensive_evs = df.nlargest(5, 'PriceEuro')[['Brand', 'Model', 'PriceEuro', 'Range_Km']]
        response = """
<div style='background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,193,7,0.1)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #ffd700;'>
    <h3 style='color: #ff9800; margin-top: 0;'>💎 Luxury & Premium EVs</h3>
"""
        for _, row in expensive_evs.iterrows():
            response += f"""
<div style='padding: 15px; margin: 10px 0; background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); 
            border-radius: 12px; box-shadow: 0 5px 15px rgba(255,193,7,0.3);'>
    <b style='color: #764ba2; font-size: 1.2em;'>{row['Brand']} {row['Model']}</b><br>
    <span style='color: #ff9800; font-size: 1.3em; font-weight: 700;'>€{row['PriceEuro']:,.0f}</span> • 
    <span style='color: #666;'>{row['Range_Km']} km range</span>
</div>"""
        response += "</div>"
        return response
    
    # Range queries
    if "range" in query_lower or "longest" in query_lower or "distance" in query_lower:
        long_range = df.nlargest(5, 'Range_Km')[['Brand', 'Model', 'Range_Km', 'PriceEuro']]
        response = """
<div style='background: linear-gradient(135deg, rgba(33,150,243,0.1), rgba(3,169,244,0.1)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #2196f3;'>
    <h3 style='color: #2196f3; margin-top: 0;'>🔋 Longest Range EVs</h3>
"""
        for _, row in long_range.iterrows():
            response += f"""
<div style='padding: 15px; margin: 10px 0; background: rgba(255,255,255,0.7); border-radius: 12px;'>
    <b style='color: #667eea; font-size: 1.2em;'>{row['Brand']} {row['Model']}</b><br>
    <span style='color: #2196f3; font-size: 1.4em; font-weight: 700;'>{row['Range_Km']} km</span> • 
    <span style='color: #666;'>€{row['PriceEuro']:,.0f}</span>
</div>"""
        response += "</div>"
        return response
    
    # Speed queries
    if "fast" in query_lower or "speed" in query_lower or "quick" in query_lower:
        fastest = df.nlargest(5, 'TopSpeed_KmH')[['Brand', 'Model', 'TopSpeed_KmH', 'AccelSec']]
        response = """
<div style='background: linear-gradient(135deg, rgba(244,67,54,0.1), rgba(233,30,99,0.1)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #f44336;'>
    <h3 style='color: #f44336; margin-top: 0;'>🏎️ Fastest EVs</h3>
"""
        for _, row in fastest.iterrows():
            response += f"""
<div style='padding: 15px; margin: 10px 0; background: rgba(255,255,255,0.7); border-radius: 12px;'>
    <b style='color: #667eea; font-size: 1.2em;'>{row['Brand']} {row['Model']}</b><br>
    <span style='color: #f44336; font-size: 1.4em; font-weight: 700;'>{row['TopSpeed_KmH']} km/h</span> • 
    <span style='color: #666;'>0-100: {row['AccelSec']}s</span>
</div>"""
        response += "</div>"
        return response
    
    # Specific brand queries
    for brand in df['Brand'].unique():
        if brand.lower() in query_lower:
            brand_cars = df[df['Brand'] == brand][['Model', 'PriceEuro', 'Range_Km', 'TopSpeed_KmH']].head(5)
            response = f"""
<div style='background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #667eea;'>
    <h3 style='color: #667eea; margin-top: 0;'>🚗 {brand} Models</h3>
"""
            for _, row in brand_cars.iterrows():
                response += f"""
<div style='padding: 15px; margin: 10px 0; background: rgba(255,255,255,0.7); border-radius: 12px;'>
    <b style='font-size: 1.1em;'>{row['Model']}</b><br>
    <span style='color: #4caf50;'>€{row['PriceEuro']:,.0f}</span> | 
    <span style='color: #2196f3;'>{row['Range_Km']} km</span> | 
    <span style='color: #f44336;'>{row['TopSpeed_KmH']} km/h</span>
</div>"""
            response += "</div>"
            return response
    
    # Statistics
    if "statistics" in query_lower or "stats" in query_lower or "summary" in query_lower:
        response = f"""
<div style='background: linear-gradient(135deg, rgba(156,39,176,0.1), rgba(233,30,99,0.1)); 
            padding: 30px; border-radius: 20px; border: 3px solid rgba(156,39,176,0.3);'>
    <h2 style='color: #9c27b0; text-align: center; margin-top: 0;'>📊 EV Dataset Statistics</h2>
    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px;'>
        <div class='metric-card'>
            <div class='metric-value'>{len(df)}</div>
            <div class='metric-label'>Total EVs</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>{df['Brand'].nunique()}</div>
            <div class='metric-label'>Brands</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>€{df['PriceEuro'].mean():,.0f}</div>
            <div class='metric-label'>Avg Price</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>{df['Range_Km'].mean():.0f} km</div>
            <div class='metric-label'>Avg Range</div>
        </div>
    </div>
</div>"""
        return response
    
    return None

def predict_ev_price(specs):
    """Predict EV price from specifications"""
    if model is None:
        return None, """
<div style='background: linear-gradient(135deg, rgba(255,152,0,0.1), rgba(255,193,7,0.1)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #ff9800;'>
    <h3 style='color: #ff9800;'>⚠️ ML Model Not Available</h3>
    <p>Please run <code>python ev_ml_analysis.py</code> first to train the model!</p>
</div>"""
    
    try:
        brand_encoded = encoders['brand'].transform([specs['brand']])[0]
        bodystyle_encoded = encoders['bodystyle'].transform([specs['body_style']])[0]
        powertrain_encoded = encoders['powertrain'].transform([specs['powertrain']])[0]
        plugtype_encoded = encoders['plugtype'].transform([specs['plug_type']])[0]
        segment_encoded = encoders['segment'].transform([specs['segment']])[0]
        rapidcharge_encoded = encoders['rapidcharge'].transform([specs['rapid_charge']])[0]
        
        features = np.array([[
            specs['accel_sec'], specs['top_speed'], specs['range_km'], specs['efficiency'],
            specs['fast_charge'], specs['seats'], brand_encoded, bodystyle_encoded,
            powertrain_encoded, plugtype_encoded, segment_encoded, rapidcharge_encoded
        ]])
        
        predicted_price = model.predict(features)[0]
        
        response = f"""
<div style='background: linear-gradient(135deg, rgba(76,175,80,0.15), rgba(139,195,74,0.15)); 
            padding: 30px; border-radius: 20px; border: 3px solid #4caf50;'>
    <h2 style='color: #4caf50; text-align: center; margin-top: 0;'>💰 Price Prediction Results</h2>
    
    <div style='background: linear-gradient(135deg, #667eea, #764ba2); 
                padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;
                box-shadow: 0 10px 30px rgba(102,126,234,0.4);'>
        <div style='color: white; font-size: 1.2em; margin-bottom: 10px;'>🎯 Predicted Price</div>
        <div style='color: white; font-size: 3em; font-weight: 700;'>€{predicted_price:,.2f}</div>
    </div>
    
    <div style='background: rgba(255,255,255,0.7); padding: 20px; border-radius: 15px; margin-top: 20px;'>
        <h4 style='color: #667eea;'>📋 Your EV Specifications:</h4>
        <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;'>
            <div><b>Brand:</b> {specs['brand']}</div>
            <div><b>Body Style:</b> {specs['body_style']}</div>
            <div><b>Acceleration:</b> {specs['accel_sec']}s</div>
            <div><b>Top Speed:</b> {specs['top_speed']} km/h</div>
            <div><b>Range:</b> {specs['range_km']} km</div>
            <div><b>Efficiency:</b> {specs['efficiency']} Wh/km</div>
            <div><b>Fast Charge:</b> {specs['fast_charge']} km/h</div>
            <div><b>Seats:</b> {specs['seats']}</div>
            <div><b>PowerTrain:</b> {specs['powertrain']}</div>
            <div><b>Segment:</b> {specs['segment']}</div>
        </div>
    </div>
    
    <div style='text-align: center; margin-top: 20px; color: #666; font-size: 0.9em;'>
        This prediction is based on analysis of {len(df)} electric vehicles
    </div>
</div>"""
        return predicted_price, response
        
    except Exception as e:
        return None, f"<div style='color: #f44336; padding: 20px; border-radius: 10px; background: rgba(244,67,54,0.1);'>❌ Error: {str(e)}</div>"

# Display chat messages with animation
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("💬 Ask me anything about electric vehicles..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response with typing indicator
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Typing animation
        with response_placeholder.container():
            st.markdown("<div class='loading-dots'>Thinking</div>", unsafe_allow_html=True)
        time.sleep(0.8)
        
        # Check for prediction request
        if any(word in prompt.lower() for word in ["predict", "price", "cost", "how much", "estimate"]) and \
           any(word in prompt.lower() for word in ["custom", "my", "new", "calculate"]):
            
            if model is None:
                response = """
<div style='background: linear-gradient(135deg, rgba(255,152,0,0.15), rgba(255,193,7,0.15)); 
            padding: 30px; border-radius: 20px; border-left: 5px solid #ff9800;'>
    <h3 style='color: #ff9800;'>⚠️ ML Model Not Available</h3>
    <p>The price prediction model hasn't been loaded. Please make sure you have:</p>
    <ol>
        <li>Run <code>python ev_ml_analysis.py</code> to train the model</li>
        <li>The model files (*.pkl) exist in the project folder</li>
    </ol>
</div>"""
            else:
                st.session_state.prediction_mode = True
                st.session_state.prediction_step = 0
                st.session_state.prediction_data = {}
                response = """
<div style='background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15)); 
            padding: 30px; border-radius: 20px; border: 3px solid #667eea;'>
    <h2 style='color: #667eea; text-align: center;'>🎯 Let's Predict Your EV Price!</h2>
    
    <div style='text-align: center; margin: 20px 0;'>
        <div style='font-size: 4em;'>🚗</div>
        <p style='font-size: 1.1em; color: #666;'>I'll guide you through 12 quick questions about your dream EV</p>
    </div>
    
    <div style='background: white; padding: 25px; border-radius: 15px; margin-top: 20px;'>
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <div style='width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        color: white; font-weight: bold; margin-right: 15px;'>1</div>
            <div>
                <h4 style='margin: 0; color: #667eea;'>Which brand?</h4>
                <p style='margin: 5px 0 0 0; color: #666; font-size: 0.9em;'>
                    e.g., Tesla, BMW, Audi, Volkswagen, Mercedes, Porsche
                </p>
            </div>
        </div>
    </div>
</div>"""
        
        elif st.session_state.prediction_mode:
            # Handle prediction workflow with beautiful UI
            step = st.session_state.prediction_step
            
            questions = [
                ("brand", "Brand", "1", None),
                ("accel_sec", "0-100 km/h acceleration", "2", "in seconds (e.g., 4.5)"),
                ("top_speed", "Top speed", "3", "in km/h (e.g., 250)"),
                ("range_km", "Range", "4", "in kilometers (e.g., 450)"),
                ("efficiency", "Efficiency", "5", "in Wh/km (e.g., 180)"),
                ("fast_charge", "Fast charging speed", "6", "in km/h (e.g., 800)"),
                ("seats", "Number of seats", "7", "(e.g., 5)"),
                ("body_style", "Body style", "8", "(Sedan, SUV, Hatchback, Liftback, etc.)"),
                ("powertrain", "PowerTrain", "9", "(AWD, FWD, or RWD)"),
                ("plug_type", "Plug type", "10", "(Type 2 CCS, Type 2 CHAdeMO, etc.)"),
                ("segment", "Segment", "11", "(A, B, C, D, E, F, S, or N)"),
                ("rapid_charge", "Rapid charging", "12", "(Yes or No)")
            ]
            
            if step < len(questions):
                key, label, num, hint = questions[step]
                
                # Validate and store input
                valid_input = True
                error_msg = ""
                
                if step > 0:  # Process previous answer
                    prev_key = questions[step-1][0]
                    try:
                        if prev_key in ['accel_sec', 'efficiency']:
                            st.session_state.prediction_data[prev_key] = float(prompt)
                        elif prev_key in ['top_speed', 'range_km', 'fast_charge', 'seats']:
                            st.session_state.prediction_data[prev_key] = int(prompt)
                        else:
                            st.session_state.prediction_data[prev_key] = prompt.strip()
                    except ValueError:
                        valid_input = False
                        error_msg = f"❌ Please enter a valid number for {questions[step-1][1]}"
                else:
                    st.session_state.prediction_data['brand'] = prompt.strip()
                
                if valid_input and error_msg == "":
                    st.session_state.prediction_step += 1
                    
                    if st.session_state.prediction_step < len(questions):
                        next_key, next_label, next_num, next_hint = questions[st.session_state.prediction_step]
                        progress = (st.session_state.prediction_step / len(questions)) * 100
                        
                        response = f"""
<div style='background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15)); 
            padding: 30px; border-radius: 20px; border: 3px solid #667eea;'>
    
    <div style='background: rgba(255,255,255,0.7); border-radius: 10px; padding: 10px; margin-bottom: 20px;'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
            <span style='font-weight: 600; color: #667eea;'>Progress</span>
            <span style='font-weight: 600; color: #667eea;'>{progress:.0f}%</span>
        </div>
        <div style='width: 100%; height: 20px; background: rgba(102,126,234,0.2); border-radius: 10px; overflow: hidden;'>
            <div style='width: {progress}%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); 
                        transition: width 0.5s ease;'></div>
        </div>
    </div>
    
    <div style='background: white; padding: 25px; border-radius: 15px;'>
        <div style='display: flex; align-items: center;'>
            <div style='width: 50px; height: 50px; background: linear-gradient(135deg, #667eea, #764ba2); 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        color: white; font-weight: bold; font-size: 1.3em; margin-right: 20px;'>{next_num}</div>
            <div style='flex: 1;'>
                <h3 style='margin: 0; color: #667eea;'>What's the {next_label}?</h3>
                <p style='margin: 5px 0 0 0; color: #666;'>{next_hint if next_hint else ''}</p>
            </div>
        </div>
    </div>
</div>"""
                    else:
                        # Make final prediction
                        _, response = predict_ev_price(st.session_state.prediction_data)
                        
                        # Reset prediction mode
                        st.session_state.prediction_mode = False
                        st.session_state.prediction_step = 0
                        
                        response += """
<div style='text-align: center; margin-top: 20px; padding: 20px; background: rgba(255,255,255,0.7); border-radius: 15px;'>
    <p style='font-size: 1.1em; color: #667eea;'>💬 Feel free to ask me anything else about EVs!</p>
</div>"""
                else:
                    response = f"""
<div style='background: linear-gradient(135deg, rgba(244,67,54,0.15), rgba(233,30,99,0.15)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #f44336;'>
    <h3 style='color: #f44336;'>{error_msg}</h3>
    <p>Please try again with the correct format.</p>
</div>"""
        
        else:
            # Normal query handling
            response = get_ev_info(prompt)
            
            if response is None:
                # General responses with beautiful UI
                if any(word in prompt.lower() for word in ["hello", "hi", "hey", "greetings"]):
                    response = """
<div style='text-align: center; padding: 30px;'>
    <div style='font-size: 4em; margin-bottom: 20px;'>👋</div>
    <h2 style='color: #667eea;'>Hello there!</h2>
    <p style='font-size: 1.2em; color: #666;'>How can I help you with electric vehicles today?</p>
</div>"""
                elif any(word in prompt.lower() for word in ["thank", "thanks", "appreciate"]):
                    response = """
<div style='text-align: center; padding: 30px;'>
    <div style='font-size: 4em; margin-bottom: 20px;'>😊</div>
    <h2 style='color: #667eea;'>You're very welcome!</h2>
    <p style='font-size: 1.2em; color: #666;'>Let me know if you need anything else!</p>
</div>"""
                elif "help" in prompt.lower():
                    response = """
<div style='background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15)); 
            padding: 30px; border-radius: 20px;'>
    <h2 style='color: #667eea; text-align: center;'>🤖 How I Can Help You</h2>
    
    <div style='display: grid; gap: 15px; margin: 30px 0;'>
        <div class='quick-action' style='background: rgba(255,255,255,0.9); color: #333; padding: 20px; border-radius: 15px;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>🔍</div>
            <b>Find EVs</b><br>
            <span style='font-size: 0.9em;'>Search by brand, price, features</span>
        </div>
        
        <div class='quick-action' style='background: rgba(255,255,255,0.9); color: #333; padding: 20px; border-radius: 15px;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>💰</div>
            <b>Predict Prices</b><br>
            <span style='font-size: 0.9em;'>Custom EV price estimation</span>
        </div>
        
        <div class='quick-action' style='background: rgba(255,255,255,0.9); color: #333; padding: 20px; border-radius: 15px;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>📊</div>
            <b>Compare Models</b><br>
            <span style='font-size: 0.9em;'>Detailed comparisons & stats</span>
        </div>
        
        <div class='quick-action' style='background: rgba(255,255,255,0.9); color: #333; padding: 20px; border-radius: 15px;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>❓</div>
            <b>Answer Questions</b><br>
            <span style='font-size: 0.9em;'>Expert EV insights</span>
        </div>
    </div>
    
    <div style='background: white; padding: 20px; border-radius: 15px; margin-top: 20px;'>
        <h4 style='color: #667eea;'>✨ Try these commands:</h4>
        <div style='color: #666;'>
            • "Show me affordable EVs under €40,000"<br>
            • "What are the fastest EVs?"<br>
            • "Tell me about Tesla models"<br>
            • "Predict price for my custom EV"<br>
            • "Show me SUVs with best range"<br>
            • "Give me statistics"
        </div>
    </div>
</div>"""
                else:
                    response = """
<div style='background: linear-gradient(135deg, rgba(156,39,176,0.15), rgba(233,30,99,0.15)); 
            padding: 30px; border-radius: 20px; text-align: center;'>
    <div style='font-size: 4em; margin-bottom: 20px;'>🤔</div>
    <h3 style='color: #9c27b0;'>Hmm, I'm not sure about that...</h3>
    <p style='color: #666; font-size: 1.1em;'>But I can help you with:</p>
    
    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 30px;'>
        <div style='background: white; padding: 20px; border-radius: 12px;'>
            <div style='font-size: 2em;'>💰</div>
            <b>Affordable EVs</b>
        </div>
        <div style='background: white; padding: 20px; border-radius: 12px;'>
            <div style='font-size: 2em;'>🏎️</div>
            <b>Fast EVs</b>
        </div>
        <div style='background: white; padding: 20px; border-radius: 12px;'>
            <div style='font-size: 2em;'>🔋</div>
            <b>Long Range</b>
        </div>
        <div style='background: white; padding: 20px; border-radius: 12px;'>
            <div style='font-size: 2em;'>🎯</div>
            <b>Price Prediction</b>
        </div>
    </div>
    
    <p style='margin-top: 30px; font-size: 1.1em; color: #667eea;'>What would you like to explore?</p>
</div>"""
        
        response_placeholder.markdown(response, unsafe_allow_html=True)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Stunning Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.2); 
                    border-radius: 15px; margin-bottom: 20px;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>⚡</div>
            <h2 style='color: white; margin: 0;'>Quick Actions</h2>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.prediction_mode = False
            st.session_state.prediction_step = 0
            st.rerun()
    
    with col2:
        if st.button("💰 Predict", use_container_width=True):
            prompt = "predict price for my custom ev"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
    
    if st.button("📊 Statistics", use_container_width=True):
        prompt = "show me statistics"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    
    if st.button("💎 Luxury EVs", use_container_width=True):
        prompt = "show me luxury evs"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    
    st.markdown("---")
    
    # Beautiful stats cards
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{len(df)}</div>
            <div class='metric-label'>Total EVs</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>{df['Brand'].nunique()}</div>
            <div class='metric-label'>Brands</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>€{df['PriceEuro'].mean():,.0f}</div>
            <div class='metric-label'>Avg Price</div>
        </div>
        """, unsafe_allow_html=True)
    
    if model is not None:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(76,175,80,0.3), rgba(139,195,74,0.3)); 
                        padding: 15px; border-radius: 12px; text-align: center; margin-top: 20px;'>
                <div style='font-size: 2em;'>✅</div>
                <b style='color: white;'>ML Model Loaded</b>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(244,67,54,0.3), rgba(233,30,99,0.3)); 
                        padding: 15px; border-radius: 12px; text-align: center; margin-top: 20px;'>
                <div style='font-size: 2em;'>❌</div>
                <b style='color: white;'>Model Not Loaded</b>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.1); 
                    border-radius: 15px;'>
            <h4 style='color: white;'>💡 Sample Questions</h4>
            <div style='text-align: left; color: rgba(255,255,255,0.9); font-size: 0.9em;'>
                • Show me affordable EVs<br>
                • What are the fastest EVs?<br>
                • Tell me about Tesla<br>
                • Show me SUVs<br>
                • Longest range EVs<br>
                • Most efficient EVs
            </div>
        </div>
        """, unsafe_allow_html=True)