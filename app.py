from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        return{
            "temperature": data['current']['temperature_2m'],
            "wind_speed": data['current']['wind_speed_10m'],
            "humidity": data['current']['relative_humidity_2m'],
            "weather_code": data['current']['weather_code']
        }
    except:
        return None

cities = {
    "Karachi" : (24.8607, 67.0011),
    "Lahore" : (31.5204, 74.3587),
    "Islamabad" : (33.6844, 73.0479),
    "Rawalpindi" : (33.5651, 73.0169),
    "Multan" : (30.1575, 71.5249),
    "Faisalabad" : (31.4504, 73.1350),
    "Quetta" : (30.1798, 66.9750),
    "Peshawar" : (34.0151, 71.5249)
}

def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "results" in data:
            return data["results"][0]["latitude"], data["results"][0]["longitude"]
    except:
        pass
    return None


def get_weather_condition(code):
    if code == 0:
        return "Clear Sky ☀️"
    elif code in [1,2,3]:
        return "Partly Cloudy ⛅"
    elif code in [45, 48]:
        return "Fog 🌫"
    elif code in [51,52,53]:
        return "Drizzle 🌦"
    elif code in [61,62,64]:
        return "Rain 🌧"
    elif code in [71,73,75]:
        return "Snow ❄"
    else:
        return "Unknown"

@app.route("/", methods=["GET", "POST"])


def index():
    weather = None
    selected_city = None
    error = None

    if request.method == "POST":
        selected_city = request.form.get("city")

        if not selected_city:
            error = "Please enter a city"
        else:
            coords = get_coordinates(selected_city)
            if coords:
                lat, lon = coords
                weather = get_weather(lat,lon)

                if weather:
                    weather["condition"] = get_weather_condition(weather["weather_code"])
            else:
                error = "city not found"

    return render_template("index.html", cities=cities.keys(), weather=weather, selected_city=selected_city, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))    

    