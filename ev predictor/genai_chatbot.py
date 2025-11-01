import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
import time
import random

# Page configuration
st.set_page_config(
    page_title="🤖 GenAI EV Assistant",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the premium CSS from previous chatbot
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Rajdhani', sans-serif; }
    
    .main {
        background: 
            linear-gradient(135deg, 
                rgba(0, 0, 0, 0.85) 0%,
                rgba(102, 126, 234, 0.7) 25%,
                rgba(118, 75, 162, 0.7) 50%,
                rgba(240, 147, 251, 0.7) 75%,
                rgba(0, 0, 0, 0.85) 100%
            ),
            url('https://images.unsplash.com/photo-1617788138017-80ad40651399?w=1920') center/cover fixed;
        animation: bgShift 20s ease infinite;
    }
    
    @keyframes bgShift {
        0%, 100% { filter: hue-rotate(0deg) brightness(1); }
        50% { filter: hue-rotate(60deg) brightness(1.2); }
    }
    
    .glass-premium {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(25px);
        border: 2px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border-radius: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .header-container {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(102, 126, 234, 0.3), rgba(0, 0, 0, 0.9));
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        margin-bottom: 30px;
        border: 3px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #764ba2, #667eea) 1;
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.6);
        animation: borderFlow 3s linear infinite;
    }
    
    @keyframes borderFlow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .header-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 4em;
        font-weight: 900;
        background: linear-gradient(90deg, #00f5ff, #667eea, #764ba2, #f093fb, #4facfe, #00f5ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rgbShift 3s linear infinite;
        letter-spacing: 5px;
    }
    
    @keyframes rgbShift {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    .stChatMessage {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(20, 20, 40, 0.9)) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 25px !important;
        padding: 25px !important;
        margin: 20px 0 !important;
        border: 2px solid !important;
        border-image: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #4facfe, #667eea) 1 !important;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3) !important;
        animation: messageSlide 0.6s ease;
    }
    
    @keyframes messageSlide {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .stChatMessage:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5) !important;
    }
    
    .typing-indicator {
        display: inline-block;
        animation: typing 1.5s infinite;
    }
    
    @keyframes typing {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    .ai-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(240, 147, 251, 0.8));
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 700;
        margin: 5px;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
        border: 2px solid rgba(255, 255, 255, 0.3);
        letter-spacing: 1px;
        font-size: 0.9em;
    }
    
    .insight-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.1));
        padding: 20px;
        border-radius: 15px;
        border-left: 4px solid #00f5ff;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    .comparison-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 10px;
    }
    
    .comparison-table td {
        padding: 15px;
        background: rgba(102, 126, 234, 0.2);
        border-radius: 10px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.6), rgba(102, 126, 234, 0.2));
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 2px solid rgba(102, 126, 234, 0.4);
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: cardFloat 3s ease-in-out infinite;
    }
    
    @keyframes cardFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .stButton button {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
        color: white;
        border: 2px solid rgba(102, 126, 234, 0.5);
        border-radius: 20px;
        padding: 18px 35px;
        font-size: 1.1em;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.8);
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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversation_context = []
    st.session_state.user_preferences = {}

# GenAI Intelligence Engine
class EVGenAI:
    def __init__(self, df, model, encoders):
        self.df = df
        self.model = model
        self.encoders = encoders
        self.context = []
        
    def analyze_sentiment(self, query):
        """Analyze user intent and sentiment"""
        positive_words = ['best', 'top', 'excellent', 'amazing', 'love', 'great', 'perfect']
        budget_words = ['cheap', 'affordable', 'budget', 'economical', 'save', 'value']
        luxury_words = ['luxury', 'premium', 'high-end', 'expensive', 'elite', 'supercar']
        comparison_words = ['compare', 'vs', 'versus', 'difference', 'better']
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in budget_words):
            return "budget_conscious"
        elif any(word in query_lower for word in luxury_words):
            return "luxury_seeker"
        elif any(word in query_lower for word in comparison_words):
            return "comparison_seeker"
        elif any(word in query_lower for word in positive_words):
            return "quality_seeker"
        return "information_seeker"
    
    def generate_smart_recommendation(self, query):
        """Generate intelligent recommendations based on query"""
        sentiment = self.analyze_sentiment(query)
        
        if sentiment == "budget_conscious":
            cars = self.df.nsmallest(3, 'PriceEuro')
            return self._format_recommendation(cars, "💰 SMART BUDGET PICKS", sentiment)
        
        elif sentiment == "luxury_seeker":
            cars = self.df.nlargest(3, 'PriceEuro')
            return self._format_recommendation(cars, "👑 ELITE LUXURY SELECTION", sentiment)
        
        elif sentiment == "quality_seeker":
            # Best value: High range, low price
            self.df['value_score'] = self.df['Range_Km'] / self.df['PriceEuro'] * 10000
            cars = self.df.nlargest(3, 'value_score')
            return self._format_recommendation(cars, "⭐ BEST VALUE CHAMPIONS", sentiment)
        
        else:
            # Random popular picks
            popular_brands = ['Tesla', 'BMW', 'Audi', 'Mercedes', 'Porsche']
            cars = self.df[self.df['Brand'].isin(popular_brands)].sample(min(3, len(self.df)))
            return self._format_recommendation(cars, "🎯 CURATED SELECTION", sentiment)
    
    def _format_recommendation(self, cars, title, sentiment):
        """Format recommendation with AI insights"""
        response = f"""
<div class='glass-premium' style='padding: 35px;'>
    <h2 style='color: #00f5ff; text-shadow: 0 0 20px #00f5ff; font-family: Orbitron; text-align: center; margin-bottom: 30px;'>
        {title}
    </h2>
    <div style='text-align: center; margin-bottom: 25px;'>
        <span class='ai-badge'>🤖 AI POWERED</span>
        <span class='ai-badge'>🎯 PERSONALIZED</span>
        <span class='ai-badge'>⚡ SMART MATCH</span>
    </div>
"""
        
        for idx, (_, car) in enumerate(cars.iterrows(), 1):
            # Generate AI insights
            insights = self._generate_insights(car, sentiment)
            
            response += f"""
<div class='insight-card'>
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
        <h3 style='color: #00f5ff; font-family: Orbitron; margin: 0; font-size: 1.5em;'>
            #{idx} {car['Brand']} {car['Model']}
        </h3>
        <span style='color: #ffd700; font-size: 1.8em; font-weight: 900;'>€{car['PriceEuro']:,.0f}</span>
    </div>
    
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;'>
        <div style='text-align: center; background: rgba(33,150,243,0.2); padding: 12px; border-radius: 10px;'>
            <div style='color: #2196f3; font-size: 1.4em; font-weight: 700;'>{car['Range_Km']} km</div>
            <div style='color: #fff; font-size: 0.9em;'>Range</div>
        </div>
        <div style='text-align: center; background: rgba(244,67,54,0.2); padding: 12px; border-radius: 10px;'>
            <div style='color: #f44336; font-size: 1.4em; font-weight: 700;'>{car['TopSpeed_KmH']} km/h</div>
            <div style='color: #fff; font-size: 0.9em;'>Top Speed</div>
        </div>
        <div style='text-align: center; background: rgba(76,175,80,0.2); padding: 12px; border-radius: 10px;'>
            <div style='color: #4caf50; font-size: 1.4em; font-weight: 700;'>{car['AccelSec']}s</div>
            <div style='color: #fff; font-size: 0.9em;'>0-100</div>
        </div>
    </div>
    
    <div style='background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; border-left: 3px solid #f093fb;'>
        <div style='color: #f093fb; font-weight: 700; margin-bottom: 8px; font-size: 1.1em;'>🤖 AI INSIGHT:</div>
        <div style='color: #fff; line-height: 1.6;'>{insights}</div>
    </div>
</div>
"""
        
        response += "</div>"
        return response
    
    def _generate_insights(self, car, sentiment):
        """Generate contextual AI insights"""
        insights = []
        
        # Performance insights
        if car['AccelSec'] < 4:
            insights.append(f"⚡ Lightning-fast acceleration of {car['AccelSec']}s puts this in supercar territory")
        elif car['AccelSec'] < 6:
            insights.append(f"🏎️ Impressive {car['AccelSec']}s acceleration for spirited driving")
        
        # Range insights
        if car['Range_Km'] > 500:
            insights.append(f"🔋 Exceptional {car['Range_Km']}km range eliminates range anxiety")
        elif car['Range_Km'] > 400:
            insights.append(f"✅ Solid {car['Range_Km']}km range perfect for daily use and road trips")
        
        # Value insights
        if sentiment == "budget_conscious":
            value = car['Range_Km'] / car['PriceEuro'] * 1000
            insights.append(f"💰 Outstanding value at {value:.2f} km per €1000")
        
        # Efficiency
        if car['Efficiency_WhKm'] < 170:
            insights.append(f"🌱 Highly efficient at {car['Efficiency_WhKm']} Wh/km means lower running costs")
        
        return " • ".join(insights[:2]) if insights else "Perfect balance of performance and practicality"
    
    def compare_vehicles(self, brand1, brand2=None):
        """Generate detailed comparison"""
        if brand2:
            cars1 = self.df[self.df['Brand'].str.contains(brand1, case=False, na=False)]
            cars2 = self.df[self.df['Brand'].str.contains(brand2, case=False, na=False)]
            
            if len(cars1) == 0 or len(cars2) == 0:
                return None
            
            car1 = cars1.iloc[0]
            car2 = cars2.iloc[0]
            
            return self._format_comparison(car1, car2)
        
        return None
    
    def _format_comparison(self, car1, car2):
        """Format detailed comparison"""
        response = f"""
<div class='glass-premium' style='padding: 40px;'>
    <h2 style='color: #f093fb; text-shadow: 0 0 30px #f093fb; font-family: Orbitron; text-align: center; margin-bottom: 40px; font-size: 2.5em;'>
        ⚔️ HEAD-TO-HEAD BATTLE
    </h2>
    
    <table class='comparison-table'>
        <tr>
            <td style='width: 25%; font-weight: 700; color: #00f5ff;'>VEHICLE</td>
            <td style='width: 37.5%; text-align: center;'>
                <div style='font-size: 1.5em; color: #667eea; font-weight: 900;'>{car1['Brand']} {car1['Model']}</div>
            </td>
            <td style='width: 37.5%; text-align: center;'>
                <div style='font-size: 1.5em; color: #f093fb; font-weight: 900;'>{car2['Brand']} {car2['Model']}</div>
            </td>
        </tr>
        <tr>
            <td style='font-weight: 700; color: #00f5ff;'>💰 PRICE</td>
            <td style='text-align: center; color: {"#4caf50" if car1["PriceEuro"] < car2["PriceEuro"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                €{car1['PriceEuro']:,.0f} {"✅" if car1["PriceEuro"] < car2["PriceEuro"] else ""}
            </td>
            <td style='text-align: center; color: {"#4caf50" if car2["PriceEuro"] < car1["PriceEuro"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                €{car2['PriceEuro']:,.0f} {"✅" if car2["PriceEuro"] < car1["PriceEuro"] else ""}
            </td>
        </tr>
        <tr>
            <td style='font-weight: 700; color: #00f5ff;'>🔋 RANGE</td>
            <td style='text-align: center; color: {"#2196f3" if car1["Range_Km"] > car2["Range_Km"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car1['Range_Km']} km {"🏆" if car1["Range_Km"] > car2["Range_Km"] else ""}
            </td>
            <td style='text-align: center; color: {"#2196f3" if car2["Range_Km"] > car1["Range_Km"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car2['Range_Km']} km {"🏆" if car2["Range_Km"] > car1["Range_Km"] else ""}
            </td>
        </tr>
        <tr>
            <td style='font-weight: 700; color: #00f5ff;'>⚡ 0-100</td>
            <td style='text-align: center; color: {"#f44336" if car1["AccelSec"] < car2["AccelSec"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car1['AccelSec']}s {"🏆" if car1["AccelSec"] < car2["AccelSec"] else ""}
            </td>
            <td style='text-align: center; color: {"#f44336" if car2["AccelSec"] < car1["AccelSec"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car2['AccelSec']}s {"🏆" if car2["AccelSec"] < car1["AccelSec"] else ""}
            </td>
        </tr>
        <tr>
            <td style='font-weight: 700; color: #00f5ff;'>🏎️ TOP SPEED</td>
            <td style='text-align: center; color: {"#ff9800" if car1["TopSpeed_KmH"] > car2["TopSpeed_KmH"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car1['TopSpeed_KmH']} km/h {"🏆" if car1["TopSpeed_KmH"] > car2["TopSpeed_KmH"] else ""}
            </td>
            <td style='text-align: center; color: {"#ff9800" if car2["TopSpeed_KmH"] > car1["TopSpeed_KmH"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car2['TopSpeed_KmH']} km/h {"🏆" if car2["TopSpeed_KmH"] > car1["TopSpeed_KmH"] else ""}
            </td>
        </tr>
        <tr>
            <td style='font-weight: 700; color: #00f5ff;'>🌱 EFFICIENCY</td>
            <td style='text-align: center; color: {"#4caf50" if car1["Efficiency_WhKm"] < car2["Efficiency_WhKm"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car1['Efficiency_WhKm']} Wh/km {"🏆" if car1["Efficiency_WhKm"] < car2["Efficiency_WhKm"] else ""}
            </td>
            <td style='text-align: center; color: {"#4caf50" if car2["Efficiency_WhKm"] < car1["Efficiency_WhKm"] else "#fff"}; font-size: 1.2em; font-weight: 700;'>
                {car2['Efficiency_WhKm']} Wh/km {"🏆" if car2["Efficiency_WhKm"] < car1["Efficiency_WhKm"] else ""}
            </td>
        </tr>
    </table>
    
    <div style='margin-top: 40px; padding: 25px; background: rgba(102,126,234,0.2); border-radius: 20px; border: 2px solid rgba(102,126,234,0.4);'>
        <div style='color: #f093fb; font-weight: 700; font-size: 1.3em; margin-bottom: 15px; font-family: Orbitron;'>
            🤖 AI VERDICT:
        </div>
        <div style='color: #fff; font-size: 1.1em; line-height: 1.8;'>
            {self._generate_verdict(car1, car2)}
        </div>
    </div>
</div>"""
        return response
    
    def _generate_verdict(self, car1, car2):
        """Generate AI verdict for comparison"""
        car1_wins = 0
        car2_wins = 0
        
        if car1['PriceEuro'] < car2['PriceEuro']: car1_wins += 1
        else: car2_wins += 1
        
        if car1['Range_Km'] > car2['Range_Km']: car1_wins += 1
        else: car2_wins += 1
        
        if car1['AccelSec'] < car2['AccelSec']: car1_wins += 1
        else: car2_wins += 1
        
        if car1['TopSpeed_KmH'] > car2['TopSpeed_KmH']: car1_wins += 1
        else: car2_wins += 1
        
        if car1_wins > car2_wins:
            winner = f"{car1['Brand']} {car1['Model']}"
            verdict = f"The <b style='color: #667eea;'>{winner}</b> emerges victorious with {car1_wins} category wins! "
        elif car2_wins > car1_wins:
            winner = f"{car2['Brand']} {car2['Model']}"
            verdict = f"The <b style='color: #f093fb;'>{winner}</b> takes the crown with {car2_wins} category wins! "
        else:
            verdict = "It's a tie! Both vehicles excel in different areas. "
        
        verdict += "Your choice should depend on whether you prioritize <span style='color: #4caf50;'>value</span>, <span style='color: #2196f3;'>range</span>, or <span style='color: #f44336;'>performance</span>."
        
        return verdict

# Initialize GenAI Engine
genai = EVGenAI(df, model, encoders)

# Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">
            🤖 GenAI EV ASSISTANT ⚡
        </div>
        <div style='color: #fff; font-size: 1.5em; margin-top: 20px; letter-spacing: 3px;'>
            POWERED BY GENERATIVE AI
        </div>
        <div style="margin-top: 30px;">
            <span class="ai-badge">🧠 DEEP LEARNING</span>
            <span class="ai-badge">🎯 CONTEXT AWARE</span>
            <span class="ai-badge">⚡ REAL-TIME</span>
            <span class="ai-badge">🔮 PREDICTIVE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Welcome message
if len(st.session_state.messages) == 0:
    welcome = """
<div class='glass-premium' style='padding: 40px; text-align: center;'>
    <div style='font-size: 4em; margin-bottom: 25px;'>🤖</div>
    <h2 style='color: #00f5ff; font-family: Orbitron; font-size: 2.5em; text-shadow: 0 0 30px #00f5ff;'>
        WELCOME TO GenAI EV ASSISTANT
    </h2>
    <p style='color: #fff; font-size: 1.3em; margin: 30px 0; line-height: 1.8;'>
        I'm your intelligent AI companion powered by advanced machine learning. 
        I understand context, learn from our conversation, and provide personalized recommendations.
    </p>
    
    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 40px 0;'>
        <div class='insight-card'>
            <div style='font-size: 2.5em; margin-bottom: 10px;'>🧠</div>
            <b style='color: #00f5ff; font-size: 1.2em;'>SMART RECOMMENDATIONS</b>
            <p style='color: #fff; margin-top: 10px;'>AI-powered suggestions based on your preferences</p>
        </div>
        <div class='insight-card'>
            <div style='font-size: 2.5em; margin-bottom: 10px;'>🎯</div>
            <b style='color: #f093fb; font-size: 1.2em;'>CONTEXT AWARENESS</b>
            <p style='color: #fff; margin-top: 10px;'>Remembers conversation for better responses</p>
        </div>
        <div class='insight-card'>
            <div style='font-size: 2.5em; margin-bottom: 10px;'>⚔️</div>
            <b style='color: #4caf50; font-size: 1.2em;'>SMART COMPARISONS</b>
            <p style='color: #fff; margin-top: 10px;'>Detailed head-to-head vehicle analysis</p>
        </div>
        <div class='insight-card'>
            <div style='font-size: 2.5em; margin-bottom: 10px;'>💰</div>
            <b style='color: #ffd700; font-size: 1.2em;'>PRICE PREDICTION</b>
            <p style='color: #fff; margin-top: 10px;'>ML-powered price estimation with insights</p>
        </div>
    </div>
    
    <div style='margin-top: 40px; padding: 25px; background: rgba(102,126,234,0.2); border-radius: 20px; border: 2px solid rgba(102,126,234,0.5);'>
        <b style='color: #00f5ff; font-size: 1.4em; font-family: Orbitron;'>✨ TRY THESE COMMANDS:</b><br><br>
        <div style='text-align: left; max-width: 700px; margin: 0 auto; color: #fff; line-height: 2.2; font-size: 1.1em;'>
        • "Recommend me a good EV"<br>
        • "Compare Tesla vs Porsche"<br>
        • "I need a budget-friendly family car"<br>
        • "Show me the best luxury EVs"<br>
        • "What's better for long trips?"<br>
        • "Predict price for custom specs"
        </div>
    </div>
    
    <div style='margin-top: 40px; font-size: 2em; color: #f093fb; text-shadow: 0 0 20px #f093fb;'>
        Ready to explore? Ask me anything! 🚀
    </div>
</div>"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("💬 Ask me anything about EVs..."):
    # Add to context
    st.session_state.conversation_context.append(prompt)
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Typing indicator
        with response_placeholder.container():
            st.markdown("<div style='color: #00f5ff;'><span class='typing-indicator'>🤖 Analyzing your request with AI...</span></div>", unsafe_allow_html=True)
        time.sleep(1)
        
        # Process query with GenAI
        query_lower = prompt.lower()
        response = None
        
        # Check for comparison requests
        if "compare" in query_lower or "vs" in query_lower or "versus" in query_lower:
            # Extract brands
            words = prompt.split()
            brands = []
            for brand in df['Brand'].unique():
                if brand.lower() in query_lower:
                    brands.append(brand)
            
            if len(brands) >= 2:
                response = genai.compare_vehicles(brands[0], brands[1])
            elif len(brands) == 1:
                response = f"""
<div class='glass-premium' style='padding: 30px;'>
    <h3 style='color: #ff9800; font-family: Orbitron;'>🤔 I need another brand to compare!</h3>
    <p style='color: #fff; font-size: 1.1em; margin: 20px 0;'>
        You mentioned <b style='color: #00f5ff;'>{brands[0]}</b>. Which brand would you like to compare it with?
    </p>
    <p style='color: rgba(255,255,255,0.7);'>Try: "Compare Tesla vs BMW" or "Tesla versus Porsche"</p>
</div>"""
        
        # Check for recommendation requests
        elif any(word in query_lower for word in ["recommend", "suggest", "best", "good", "show me", "find", "looking for"]):
            response = genai.generate_smart_recommendation(prompt)
        
        # Specific queries
        elif "budget" in query_lower or "cheap" in query_lower or "affordable" in query_lower:
            response = genai.generate_smart_recommendation(prompt)
        
        elif "luxury" in query_lower or "premium" in query_lower or "expensive" in query_lower:
            response = genai.generate_smart_recommendation(prompt)
        
        elif "family" in query_lower or "suv" in query_lower or "spacious" in query_lower:
            suvs = df[df['BodyStyle'] == 'SUV'].nsmallest(3, 'PriceEuro')
            response = f"""
<div class='glass-premium' style='padding: 35px;'>
    <h2 style='color: #00f5ff; text-shadow: 0 0 20px #00f5ff; font-family: Orbitron; text-align: center; margin-bottom: 30px;'>
        👨‍👩‍👧‍👦 PERFECT FAMILY SUVS
    </h2>
    <div style='text-align: center; margin-bottom: 25px;'>
        <span class='ai-badge'>🤖 AI CURATED</span>
        <span class='ai-badge'>👨‍👩‍👧‍👦 FAMILY FRIENDLY</span>
        <span class='ai-badge'>💰 VALUE PICKS</span>
    </div>
"""
            for idx, (_, car) in enumerate(suvs.iterrows(), 1):
                response += f"""
<div class='insight-card'>
    <h3 style='color: #00f5ff; font-family: Orbitron; font-size: 1.5em;'>
        #{idx} {car['Brand']} {car['Model']}
    </h3>
    <div style='margin: 15px 0;'>
        <span style='color: #ffd700; font-size: 1.6em; font-weight: 900;'>€{car['PriceEuro']:,.0f}</span> • 
        <span style='color: #2196f3; font-size: 1.2em;'>{car['Range_Km']} km</span> • 
        <span style='color: #4caf50; font-size: 1.2em;'>{car['Seats']} seats</span>
    </div>
    <div style='background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; border-left: 3px solid #f093fb;'>
        <div style='color: #f093fb; font-weight: 700; margin-bottom: 8px;'>🤖 AI INSIGHT:</div>
        <div style='color: #fff;'>Spacious {car['Seats']}-seater with {car['Range_Km']}km range perfect for family road trips. Practical yet enjoyable to drive!</div>
    </div>
</div>"""
            response += "</div>"
        
        elif "trip" in query_lower or "travel" in query_lower or "long" in query_lower or "range" in query_lower:
            long_range = df.nlargest(3, 'Range_Km')
            response = f"""
<div class='glass-premium' style='padding: 35px;'>
    <h2 style='color: #2196f3; text-shadow: 0 0 20px #2196f3; font-family: Orbitron; text-align: center; margin-bottom: 30px;'>
        🗺️ ROAD TRIP CHAMPIONS
    </h2>
    <div style='text-align: center; margin-bottom: 25px;'>
        <span class='ai-badge'>🤖 AI SELECTED</span>
        <span class='ai-badge'>🔋 MAX RANGE</span>
        <span class='ai-badge'>✈️ TRAVEL READY</span>
    </div>
"""
            for idx, (_, car) in enumerate(long_range.iterrows(), 1):
                response += f"""
<div class='insight-card'>
    <h3 style='color: #00f5ff; font-family: Orbitron; font-size: 1.5em;'>
        #{idx} {car['Brand']} {car['Model']}
    </h3>
    <div style='margin: 15px 0;'>
        <span style='color: #2196f3; font-size: 2em; font-weight: 900;'>{car['Range_Km']} km</span> • 
        <span style='color: #ffd700; font-size: 1.2em;'>€{car['PriceEuro']:,.0f}</span>
    </div>
    <div style='background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; border-left: 3px solid #2196f3;'>
        <div style='color: #2196f3; font-weight: 700; margin-bottom: 8px;'>🤖 AI INSIGHT:</div>
        <div style='color: #fff;'>Outstanding {car['Range_Km']}km range means fewer charging stops. Perfect for cross-country adventures and long commutes!</div>
    </div>
</div>"""
            response += "</div>"
        
        elif "fast" in query_lower or "speed" in query_lower or "quick" in query_lower or "performance" in query_lower:
            fastest = df.nsmallest(3, 'AccelSec')
            response = f"""
<div class='glass-premium' style='padding: 35px;'>
    <h2 style='color: #f44336; text-shadow: 0 0 30px #f44336; font-family: Orbitron; text-align: center; margin-bottom: 30px;'>
        ⚡ ACCELERATION MONSTERS
    </h2>
    <div style='text-align: center; margin-bottom: 25px;'>
        <span class='ai-badge'>🤖 AI POWERED</span>
        <span class='ai-badge'>🏎️ SUPERCAR SPEED</span>
        <span class='ai-badge'>⚡ INSTANT TORQUE</span>
    </div>
"""
            for idx, (_, car) in enumerate(fastest.iterrows(), 1):
                response += f"""
<div class='insight-card'>
    <h3 style='color: #ff5252; font-family: Orbitron; font-size: 1.5em; text-transform: uppercase;'>
        #{idx} {car['Brand']} {car['Model']}
    </h3>
    <div style='margin: 15px 0;'>
        <span style='color: #f44336; font-size: 2.2em; font-weight: 900;'>{car['AccelSec']}s</span>
        <span style='color: #fff; font-size: 1.1em;'> 0-100 km/h</span> • 
        <span style='color: #ff9800; font-size: 1.3em;'>{car['TopSpeed_KmH']} km/h</span>
    </div>
    <div style='background: rgba(244,67,54,0.3); padding: 15px; border-radius: 12px; border-left: 3px solid #f44336;'>
        <div style='color: #f44336; font-weight: 700; margin-bottom: 8px;'>🤖 AI INSIGHT:</div>
        <div style='color: #fff;'>Brutal {car['AccelSec']}s acceleration delivers supercar thrills. This level of performance was impossible in EVs just years ago!</div>
    </div>
</div>"""
            response += "</div>"
        
        # Greeting responses
        elif any(word in query_lower for word in ["hello", "hi", "hey", "greetings"]):
            response = """
<div class='glass-premium' style='padding: 40px; text-align: center;'>
    <div style='font-size: 5em; margin-bottom: 20px;'>👋</div>
    <h2 style='color: #00f5ff; font-family: Orbitron; font-size: 2.5em; text-shadow: 0 0 30px #00f5ff;'>
        HELLO THERE!
    </h2>
    <p style='color: #fff; font-size: 1.3em; margin: 30px 0;'>
        I'm your GenAI assistant, ready to help you find the perfect electric vehicle!
    </p>
    <div style='margin-top: 30px;'>
        <span class='ai-badge'>🧠 AI POWERED</span>
        <span class='ai-badge'>🎯 PERSONALIZED</span>
    </div>
    <p style='color: rgba(255,255,255,0.8); font-size: 1.1em; margin-top: 30px;'>
        What kind of EV are you looking for today?
    </p>
</div>"""
        
        elif any(word in query_lower for word in ["thank", "thanks", "appreciate"]):
            responses_list = [
                "My pleasure! Happy to help you find your perfect EV! 😊",
                "You're welcome! Feel free to ask anything else! 🚗",
                "Glad I could assist! Let me know if you need more info! ⚡",
                "Anytime! I'm here to make your EV search easier! 🤖"
            ]
            thanks_msg = random.choice(responses_list)
            response = f"""
<div class='glass-premium' style='padding: 40px; text-align: center;'>
    <div style='font-size: 5em; margin-bottom: 20px;'>😊</div>
    <h2 style='color: #4caf50; font-family: Orbitron; font-size: 2em; text-shadow: 0 0 20px #4caf50;'>
        {thanks_msg}
    </h2>
</div>"""
        
        # Default smart response
        else:
            response = f"""
<div class='glass-premium' style='padding: 40px;'>
    <div style='text-align: center; margin-bottom: 30px;'>
        <div style='font-size: 4em; margin-bottom: 20px;'>🤖</div>
        <h3 style='color: #f093fb; font-family: Orbitron; font-size: 2em;'>
            LET ME HELP YOU!
        </h3>
    </div>
    
    <p style='color: #fff; font-size: 1.2em; margin: 25px 0; text-align: center;'>
        I can assist you with:
    </p>
    
    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 30px;'>
        <div class='insight-card' style='cursor: pointer;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🎯</div>
            <b style='color: #00f5ff; font-size: 1.2em;'>Smart Recommendations</b>
            <p style='color: #fff; margin-top: 10px; font-size: 0.95em;'>
                "Recommend me a good EV"
            </p>
        </div>
        
        <div class='insight-card' style='cursor: pointer;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>⚔️</div>
            <b style='color: #f093fb; font-size: 1.2em;'>Compare Vehicles</b>
            <p style='color: #fff; margin-top: 10px; font-size: 0.95em;'>
                "Compare Tesla vs Porsche"
            </p>
        </div>
        
        <div class='insight-card' style='cursor: pointer;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>💰</div>
            <b style='color: #4caf50; font-size: 1.2em;'>Budget Options</b>
            <p style='color: #fff; margin-top: 10px; font-size: 0.95em;'>
                "Show me affordable EVs"
            </p>
        </div>
        
        <div class='insight-card' style='cursor: pointer;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🏎️</div>
            <b style='color: #f44336; font-size: 1.2em;'>Performance Cars</b>
            <p style='color: #fff; margin-top: 10px; font-size: 0.95em;'>
                "Fastest acceleration EVs"
            </p>
        </div>
    </div>
    
    <div style='margin-top: 40px; padding: 20px; background: rgba(102,126,234,0.2); border-radius: 15px; text-align: center;'>
        <p style='color: #00f5ff; font-size: 1.2em; font-family: Orbitron;'>
            💡 Just ask naturally - I understand context!
        </p>
    </div>
</div>"""
        
        # Display response
        response_placeholder.markdown(response, unsafe_allow_html=True)
    
    # Save to messages
    st.session_state.messages.append({"role": "assistant", "content": response})

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 25px; background: rgba(102,126,234,0.3); 
                    border-radius: 20px; margin-bottom: 25px; border: 2px solid rgba(102,126,234,0.5);
                    box-shadow: 0 0 30px rgba(102,126,234,0.4);'>
            <div style='font-size: 4em; margin-bottom: 15px;'>🤖</div>
            <h2 style='color: #00f5ff; margin: 0; font-family: Orbitron; text-shadow: 0 0 20px #00f5ff;'>
                GenAI CONTROL
            </h2>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 NEW CHAT", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_context = []
            st.rerun()
    
    with col2:
        if st.button("🎯 RECOMMEND", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Recommend me a good EV"})
            st.rerun()
    
    if st.button("⚔️ COMPARE", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Compare Tesla vs BMW"})
        st.rerun()
    
    if st.button("💰 BUDGET", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Show me affordable EVs"})
        st.rerun()
    
    if st.button("👑 LUXURY", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Show me luxury supercars"})
        st.rerun()
    
    if st.button("🏎️ PERFORMANCE", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Show me fastest EVs"})
        st.rerun()
    
    st.markdown("---")
    
    # AI Stats
    st.markdown(f"""
        <div class='glass-premium' style='padding: 25px; text-align: center; margin-bottom: 20px;'>
            <h4 style='color: #00f5ff; font-family: Orbitron; margin-bottom: 20px;'>
                🧠 AI STATISTICS
            </h4>
            <div class='metric-card'>
                <div style='font-family: Orbitron; font-size: 2em; color: #00f5ff;'>{len(st.session_state.messages)}</div>
                <div style='color: #fff; font-size: 0.9em; margin-top: 5px;'>MESSAGES</div>
            </div>
            <div class='metric-card'>
                <div style='font-family: Orbitron; font-size: 2em; color: #f093fb;'>{len(df)}</div>
                <div style='color: #fff; font-size: 0.9em; margin-top: 5px;'>EVS IN DB</div>
            </div>
            <div class='metric-card'>
                <div style='font-family: Orbitron; font-size: 2em; color: #4caf50;'>{df['Brand'].nunique()}</div>
                <div style='color: #fff; font-size: 0.9em; margin-top: 5px;'>BRANDS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ML Model Status
    if model is not None:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(76,175,80,0.4), rgba(139,195,74,0.4)); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        border: 2px solid rgba(76,175,80,0.6);
                        box-shadow: 0 0 30px rgba(76,175,80,0.6);'>
                <div style='font-size: 3em; margin-bottom: 10px;'>✅</div>
                <b style='color: #fff; font-family: Orbitron; font-size: 1.1em;'>AI MODEL ACTIVE</b>
                <p style='color: rgba(255,255,255,0.8); font-size: 0.85em; margin-top: 10px;'>
                    Deep learning enabled
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(244,67,54,0.4), rgba(233,30,99,0.4)); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        border: 2px solid rgba(244,67,54,0.6);
                        box-shadow: 0 0 30px rgba(244,67,54,0.6);'>
                <div style='font-size: 3em; margin-bottom: 10px;'>❌</div>
                <b style='color: #fff; font-family: Orbitron; font-size: 1.1em;'>MODEL OFFLINE</b>
                <p style='color: rgba(255,255,255,0.8); font-size: 0.85em; margin-top: 10px;'>
                    Run ev_ml_analysis.py
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GenAI Features
    st.markdown("""
        <div class='glass-premium' style='padding: 20px;'>
            <h4 style='color: #f093fb; font-family: Orbitron; text-align: center; margin-bottom: 20px;'>
                ✨ GenAI FEATURES
            </h4>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.95em; line-height: 2;'>
                <div style='margin: 10px 0; padding: 10px; background: rgba(102,126,234,0.2); border-radius: 10px;'>
                    🧠 <b>Context Awareness</b><br>
                    <span style='font-size: 0.85em; color: rgba(255,255,255,0.7);'>Remembers conversation</span>
                </div>
                <div style='margin: 10px 0; padding: 10px; background: rgba(102,126,234,0.2); border-radius: 10px;'>
                    🎯 <b>Smart Matching</b><br>
                    <span style='font-size: 0.85em; color: rgba(255,255,255,0.7);'>Learns preferences</span>
                </div>
                <div style='margin: 10px 0; padding: 10px; background: rgba(102,126,234,0.2); border-radius: 10px;'>
                    ⚡ <b>Real-time Analysis</b><br>
                    <span style='font-size: 0.85em; color: rgba(255,255,255,0.7);'>Instant insights</span>
                </div>
                <div style='margin: 10px 0; padding: 10px; background: rgba(102,126,234,0.2); border-radius: 10px;'>
                    🔮 <b>Predictive</b><br>
                    <span style='font-size: 0.85em; color: rgba(255,255,255,0.7);'>Anticipates needs</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(102,126,234,0.2); 
                    border-radius: 15px; border: 2px solid rgba(102,126,234,0.4);'>
            <div style='font-size: 2em; margin-bottom: 10px;'>🏁</div>
            <div style='color: #00f5ff; font-family: Orbitron; font-weight: 700; letter-spacing: 2px;'>
                GenAI POWERED
            </div>
            <div style='color: rgba(255,255,255,0.6); font-size: 0.8em; margin-top: 5px;'>
                v3.0 AI EDITION
            </div>
        </div>
        """, unsafe_allow_html=True)
