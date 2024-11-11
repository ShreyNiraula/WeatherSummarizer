from flask import request, jsonify, render_template
from app.weather import fetch_weather_data
from app.prompt import analyze_weather
from app.database import save_user_to_db, get_all_subscribers
from app.alert import send_alert_to_users

# Initialize the blueprint (if using Blueprints in the future)
# from flask import Blueprint
# weather_blueprint = Blueprint('weather', __name__)

# API endpoint to fetch weather data and analyze it
def get_weather():

    weather_data = fetch_weather_data()
    prompt, analysis = analyze_weather(weather_data)

    # Prepare data for the template
    hourly_data = zip(
        weather_data["hourly"]["time"],
        weather_data["hourly"]["temperature_2m"],
        weather_data["hourly"]["precipitation_probability"],
        weather_data["hourly"]["rain"],
        weather_data["hourly"]["wind_speed_10m"]
    )

    return render_template(
        'index.html',
        weather_data=hourly_data,
        analysis=analysis
    )
    # return jsonify({
    #     'weather_data': weather_data,
    #     'analysis': analysis,
    #     'prompt': prompt
    # })

# API endpoint to handle user subscription
def subscribe():
    email = request.form['email']
    username = request.form['username']
    save_user_to_db(email, username)
    return jsonify({'message': 'Subscription successful!'})

# Endpoint to trigger alert (can be scheduled or triggered manually)
def trigger_alert():
    weather_data = fetch_weather_data()
    analysis = analyze_weather(weather_data)

    if "heavy rainfall" in analysis.lower() or "hurricane" in analysis.lower():
        send_alert_to_users(analysis)
        return jsonify({"message": "Alert triggered successfully!"})
    else:
        return jsonify({"message": "No alert needed."})
