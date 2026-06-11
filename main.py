from security_enhancements import encrypt_data, decrypt_data, sanitize_input, verify_mfa_code
import streamlit as st
import base64
from travel_guide_helper import load_all_pdfs, get_weather, get_currency_rate, get_travel_news
from post_generator import generate_travel_guidance
import re
from flask import Flask, request, jsonify
import threading
import requests

# Function to load and encode the background image for the chat history box
def set_chatbox_background(image_file):
    with open(image_file, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .chat-container {{
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background-image: url("data:image/jpg;base64,{base64_image}");
            background-size: cover;
            margin-bottom: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
# Set the background image for the chat history box
set_chatbox_background("data/static/ind.jpg")  # Ensure this image exists

app = Flask(__name__)

def sanitize_input(value):
    return value.strip() if value else ""

def generate_token(username):
    return f"token_for_{username}"



@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = sanitize_input(data.get("username"))
    password = sanitize_input(data.get("password"))
    
    # Check user credentials (dummy check, replace with DB validation)
    if username == "admin" and password == "securepassword":
        token = generate_token(username)
        return jsonify({"message": "Login successful", "token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

def run_flask():
    app.run(debug=True, use_reloader=False)

threading.Thread(target=run_flask, daemon=True).start()



# Load and cache PDF content
@st.cache_data
def load_cached_pdfs(directory_path):
    return load_all_pdfs(directory_path)

pdf_directory = "data/travel_guides/"
pdf_data = load_cached_pdfs(pdf_directory)

# Initialize session state for chat history and input tracking
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "last_query" not in st.session_state:
    st.session_state["last_query"] = ""
if "chat_input" not in st.session_state:
    st.session_state["chat_input"] = ""

def extract_city_from_query(query):
    """Extract city name from the user's query if it asks about weather."""
    weather_keywords = ["weather", "temperature", "forecast"]
    if any(keyword in query.lower() for keyword in weather_keywords):
        match = re.search(r"weather in ([a-zA-Z\s]+)", query, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def handle_submit():
    """Handle submission of the chat input."""
    if st.session_state["chat_input"]:
        user_query = st.session_state["chat_input"]
        st.session_state["chat_input"] = ""  # Clear input field immediately after submission
        process_query(user_query)

def process_query(query):
    """Process the user's query and generate a response."""
    city = extract_city_from_query(query)  # Extract city for weather-related queries
    weather_data = None

    if city:
        # Fetch weather data dynamically
        with st.spinner(f"Fetching weather for {city}..."):
            weather_data = get_weather(city)
            if "error" in weather_data:
                response = f"Sorry, I couldn't fetch the weather for {city}. Please check the city name or try again."
            else:
                response = f"The current weather in {city} is {weather_data['temperature']}°C with {weather_data['weather']}."
            st.session_state["chat_history"].append({"user": query, "bot": response})
            st.rerun()

    # Generate bot response using PDF data and Llama model
    with st.spinner("Chatbot is thinking..."):
        response = generate_travel_guidance(query, pdf_data, weather_data, st.session_state["chat_history"])

    # Append user query and bot response to chat history
    st.session_state["chat_history"].append({"user": query, "bot": response})
    st.rerun()

def main():
    # Header
    st.markdown("<h1 style='text-align: center; color: white;'>IntelliTravel</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white;'>Your AI-Powered Travel Guidance System 🌍</h4>", unsafe_allow_html=True)

    # Sidebar for additional features
    with st.sidebar:
        st.header("Quick Access")
    
    # Link to Train Schedule Page
    if st.button("Train Schedule 🚆"):
        st.switch_page("pages/train_schedule.py")

    st.subheader("Weather")
    city = st.text_input("Enter city for weather:", key="weather_city")
    if city:
        weather_data = get_weather(city)
        if "error" in weather_data:
            st.error(f"Could not fetch weather for {city}.")
        else:
            st.success(f"Weather in {city}: {weather_data['temperature']}°C, {weather_data['weather']}")

    st.subheader("Currency Conversion")
    from_currency = st.text_input("From Currency (e.g., USD):", key="from_currency")
    to_currency = st.text_input("To Currency (e.g., INR):", key="to_currency")
    if from_currency and to_currency:
        rate = get_currency_rate(from_currency, to_currency)
        if "error" in rate:
            st.error(f"Could not fetch currency rate.")
        else:
            st.success(f"1 {from_currency} = {rate['rate']} {to_currency}")

    st.subheader("Travel News")
    if st.button("Get Latest Travel News"):
        news = get_travel_news()
        if "error" in news:
            st.error("Could not fetch travel news.")
        else:
            for item in news:
                st.write(f"**{item['title']}**")
                st.write(item['description'])
                st.write(f"[Read more]({item['url']})")
                st.write("---")    

    # Display chat history dynamically
    with st.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for chat in st.session_state["chat_history"]:
            user_message = f"<div style='background-color: rgba(0, 123, 255, 0.9); color: white; padding: 10px 15px; border-radius: 15px; margin: 20px 0 10px auto; float: right; margin-right: 0;align-self: flex-end; margin-left: 100px; word-wrap: break-word; display: inline-block;'>{chat['user']}</div>"
            bot_message = f"<div style='background-color: rgba(255, 255, 255, 0.8); color: black; padding: 10px 15px; border-radius: 15px; margin: 10px 0 20px ; margin-right: 50px; word-wrap: break-word; display: inline-block;'>{chat['bot']}</div>"
            
            st.markdown(user_message, unsafe_allow_html=True)
            st.markdown(bot_message, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Chat input box
    st.text_input(
        "Type your question here:",
        key="chat_input",
        placeholder="Ask about destinations, travel tips, or general queries...",
        on_change=handle_submit,  # Trigger processing on Enter
    )

if __name__ == "__main__":
    main()





