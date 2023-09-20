from flask import Flask, render_template, request
import requests
import time
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

def get_weather(city):
    api_key = "06c921750b9a82d8f5d1294e1586276f"
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    json_data = requests.get(api_url).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))

    return {
        'condition': condition,
        'temp': temp,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'pressure': pressure,
        'humidity': humidity,
        'wind': wind,
        'sunrise': sunrise,
        'sunset': sunset
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)

    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
