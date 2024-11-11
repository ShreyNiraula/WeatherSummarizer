import requests
import sqlite3
from flask import Flask, jsonify, request, render_template
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Open-Meteo API endpoint and parameters
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 34.7304,
    "longitude": -86.5859,
    "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "rain", "wind_speed_10m"],
    "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
    "timezone": "America/Chicago",
    "forecast_days": 1
}

API_KEY = "AIzaSyCUKl3H8GOQnVlxgiU35oSS-_h_fzgqEzE"
genai.configure(api_key="AIzaSyCUKl3H8GOQnVlxgiU35oSS-_h_fzgqEzE")

# Function to fetch weather data from Open-Meteo API
def fetch_weather_data():
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


# Function to analyze weather data using ChatGPT
def analyze_weather(data):
    # Extract relevant information from API response
    hourly_data = data.get("hourly", {})
    precipitation_probabilities = hourly_data.get("precipitation_probability", [])
    rain_values = hourly_data.get("rain", [])
    wind_speeds = hourly_data.get("wind_speed_10m", [])

    # Formulate prompt for ChatGPT API
    prompt = f"""
    Given the following weather data prediction for today:
    - Precipitation probabilities over the next few hours: {precipitation_probabilities}
    - Rain values over the next few hours: {rain_values}
    - Wind speeds over the next few hours: {wind_speeds}

    Determine if there is a high chance of heavy rainfall or hurricane conditions. If so, explain why and suggest alerting users.
    Also, give suggestion within 100 words.
    """

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(
        history=[]
    )
    response = chat_session.send_message(prompt)


    return prompt, response.text


# Function to save user to SQLite database
def save_user_to_db(email, username):
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, username TEXT)")

    # Insert user if not already present
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (email, username) VALUES (?, ?)", (email, username))
        conn.commit()
    conn.close()


# Function to fetch all subscribers
def get_all_subscribers():
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    subscribers = cursor.fetchall()
    conn.close()
    return subscribers


# Function to send alert to users
def send_alert_to_users(alert_message):
    subscribers = get_all_subscribers()
    for subscriber in subscribers:
        # Example sending email (this can be implemented using an email service)
        email = subscriber[0]
        print(f"Sending alert to {email}: {alert_message}")
        # Example: Send email logic goes here
        # send_email(email, alert_message)


# API endpoint to fetch weather data and analyze it
@app.route('/', methods=['GET'])
def get_weather():
    weather_data = fetch_weather_data()
    prompt, analysis = analyze_weather(weather_data)
    return jsonify({
        'weather_data': weather_data,
        'analysis': analysis,
        'prompt': prompt
    })


# API endpoint to handle user subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    username = request.form['username']
    save_user_to_db(email, username)
    return jsonify({'message': 'Subscription successful!'})


# Endpoint to trigger alert (can be scheduled or triggered manually)
@app.route('/trigger_alert', methods=['POST'])
def trigger_alert():
    weather_data = fetch_weather_data()
    analysis = analyze_weather(weather_data)

    if "heavy rainfall" in analysis.lower() or "hurricane" in analysis.lower():
        send_alert_to_users(analysis)
        return jsonify({"message": "Alert triggered successfully!"})
    else:
        return jsonify({"message": "No alert needed."})


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
