import streamlit as st
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Function to get weather info
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"Weather in {city}: {weather}, {temp}°C"
    else:
        return "Weather data not available for the selected location."

# Function to generate itinerary using Gemini
def generate_itinerary(destination, days, interests):
    prompt = f"""
    Plan a detailed {days}-day travel itinerary for a trip to {destination}.
    Focus on these interests: {interests}.
    Include places to visit each day, local foods to try, and tips for travelers.
    """
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating itinerary: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="AI Trip Planner", layout="centered")
st.title("🗺️ AI Trip Planner with Weather")

# Add tagline
st.markdown("<h3 style='text-align: center; color: #4CAF50;'>Plan Your Trip With One-Click</h3>", unsafe_allow_html=True)

with st.form("trip_form"):
    destination = st.text_input("🌍 Destination")
    days = st.number_input("📅 Number of Days", min_value=1, max_value=30, value=5)
    interests = st.text_input("🎯 Interests (e.g., beaches, food, history)")
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    with st.spinner("✈️ Generating your itinerary..."):
        itinerary = generate_itinerary(destination, days, interests)
        weather = get_weather(destination)

    st.subheader("🧳 Generated Itinerary")
    st.markdown(itinerary)
    st.subheader("⛅ Weather Information")
    st.markdown(weather)
