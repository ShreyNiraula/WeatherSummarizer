import google.generativeai as genai
from config import Config

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