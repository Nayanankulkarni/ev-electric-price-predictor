import pickle
import pandas as pd
import numpy as np

# Load trained model and preprocessing objects
print("Loading trained model and preprocessors...")
with open('ev_price_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

print("✅ Model loaded successfully!\n")

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================
def predict_ev_price(
    brand, model_name, accel_sec, top_speed_kmh, range_km, 
    efficiency_whkm, fast_charge_kmh, seats, body_style, 
    powertrain, plug_type, segment, rapid_charge
):
    """
    Predict the price of an electric vehicle based on its specifications.
    
    Parameters:
    -----------
    brand : str - Car brand (e.g., 'Tesla', 'BMW')
    model_name : str - Model name (for display only)
    accel_sec : float - 0-100 km/h acceleration in seconds
    top_speed_kmh : int - Top speed in km/h
    range_km : int - Range in kilometers
    efficiency_whkm : int - Efficiency in Wh/km
    fast_charge_kmh : int - Fast charging speed in km/h
    seats : int - Number of seats
    body_style : str - Body style (Sedan, SUV, Hatchback, etc.)
    powertrain : str - Powertrain type (AWD, FWD, RWD)
    plug_type : str - Plug type (Type 2 CCS, Type 2, etc.)
    segment : str - Market segment (A, B, C, D, E, F, S, N)
    rapid_charge : str - Rapid charge availability (Yes/No)
    
    Returns:
    --------
    float - Predicted price in Euros
    """
    
    try:
        # Encode categorical variables
        brand_encoded = encoders['brand'].transform([brand])[0]
        bodystyle_encoded = encoders['bodystyle'].transform([body_style])[0]
        powertrain_encoded = encoders['powertrain'].transform([powertrain])[0]
        plugtype_encoded = encoders['plugtype'].transform([plug_type])[0]
        segment_encoded = encoders['segment'].transform([segment])[0]
        rapidcharge_encoded = encoders['rapidcharge'].transform([rapid_charge])[0]
        
        # Create feature array
        features = np.array([[
            accel_sec, top_speed_kmh, range_km, efficiency_whkm,
            fast_charge_kmh, seats, brand_encoded, bodystyle_encoded,
            powertrain_encoded, plugtype_encoded, segment_encoded,
            rapidcharge_encoded
        ]])
        
        # Predict
        predicted_price = model.predict(features)[0]
        
        return predicted_price
        
    except Exception as e:
        print(f"❌ Error during prediction: {str(e)}")
        return None

# ============================================================================
# EXAMPLE PREDICTIONS
# ============================================================================
print("="*80)
print("🔮 EV PRICE PREDICTION EXAMPLES")
print("="*80)

# Example 1: Tesla Model 3
print("\n1. Tesla Model 3 Long Range")
print("-"*80)
price1 = predict_ev_price(
    brand='Tesla',
    model_name='Model 3 Long Range',
    accel_sec=4.6,
    top_speed_kmh=233,
    range_km=450,
    efficiency_whkm=161,
    fast_charge_kmh=940,
    seats=5,
    body_style='Sedan',
    powertrain='AWD',
    plug_type='Type 2 CCS',
    segment='D',
    rapid_charge='Yes'
)
print(f"   Predicted Price: €{price1:,.2f}")
print(f"   Actual Price: €55,480")

# Example 2: BMW iX3
print("\n2. BMW iX3")
print("-"*80)
price2 = predict_ev_price(
    brand='BMW',
    model_name='iX3',
    accel_sec=6.8,
    top_speed_kmh=180,
    range_km=360,
    efficiency_whkm=206,
    fast_charge_kmh=560,
    seats=5,
    body_style='SUV',
    powertrain='RWD',
    plug_type='Type 2 CCS',
    segment='D',
    rapid_charge='Yes'
)
print(f"   Predicted Price: €{price2:,.2f}")
print(f"   Actual Price: €68,040")

# Example 3: Volkswagen ID.3
print("\n3. Volkswagen ID.3 Pro")
print("-"*80)
price3 = predict_ev_price(
    brand='Volkswagen',
    model_name='ID.3 Pro',
    accel_sec=9.0,
    top_speed_kmh=160,
    range_km=350,
    efficiency_whkm=166,
    fast_charge_kmh=490,
    seats=5,
    body_style='Hatchback',
    powertrain='RWD',
    plug_type='Type 2 CCS',
    segment='C',
    rapid_charge='Yes'
)
print(f"   Predicted Price: €{price3:,.2f}")
print(f"   Actual Price: €33,000")

# ============================================================================
# CUSTOM PREDICTION
# ============================================================================
print("\n" + "="*80)
print("🚗 PREDICT YOUR CUSTOM EV PRICE")
print("="*80)

def get_user_prediction():
    """Interactive function to get user input and predict price"""
    
    print("\nEnter vehicle specifications:")
    print("-"*80)
    
    try:
        brand = input("Brand (e.g., Tesla, BMW, Audi): ").strip()
        model_name = input("Model name: ").strip()
        accel_sec = float(input("0-100 km/h acceleration (seconds): "))
        top_speed_kmh = int(input("Top speed (km/h): "))
        range_km = int(input("Range (km): "))
        efficiency_whkm = int(input("Efficiency (Wh/km): "))
        fast_charge_kmh = int(input("Fast charging speed (km/h): "))
        seats = int(input("Number of seats: "))
        body_style = input("Body style (Sedan/SUV/Hatchback/etc.): ").strip()
        powertrain = input("Powertrain (AWD/FWD/RWD): ").strip()
        plug_type = input("Plug type (Type 2 CCS/Type 2 CHAdeMO/etc.): ").strip()
        segment = input("Segment (A/B/C/D/E/F/S/N): ").strip()
        rapid_charge = input("Rapid charge (Yes/No): ").strip()
        
        predicted_price = predict_ev_price(
            brand, model_name, accel_sec, top_speed_kmh, range_km,
            efficiency_whkm, fast_charge_kmh, seats, body_style,
            powertrain, plug_type, segment, rapid_charge
        )
        
        if predicted_price:
            print("\n" + "="*80)
            print(f"💰 PREDICTED PRICE: €{predicted_price:,.2f}")
            print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please ensure all inputs are in the correct format.")

# Uncomment the line below to enable interactive prediction
# get_user_prediction()

print("\n✨ Prediction script ready!")
print("Use the predict_ev_price() function to make predictions.")
print("Or uncomment get_user_prediction() for interactive mode.")