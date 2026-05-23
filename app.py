import os
import time
from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

QUOTE_API = "https://api.quotable.io/random"
WEATHER_API = "https://wttr.info/{location}?format=%C+%t"
_quote_cache = {"quote": None, "timestamp": 0}
_weather_cache = {"weather": None, "timestamp": 0}
CACHE_TTL = 30  # seconds

def get_quote():
    now = time.time()
    if _quote_cache["quote"] and (now - _quote_cache["timestamp"] < CACHE_TTL):
        return _quote_cache["quote"]
    try:
        resp = requests.get(QUOTE_API, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            quote = f"{data['content']} — {data['author']}"
            _quote_cache["quote"] = quote
            _quote_cache["timestamp"] = now
            return quote
    except Exception:
        pass
    return "Keep pushing forward. — Hermes"

def get_weather():
    now = time.time()
    location = os.getenv("DEFAULT_LOCATION", "Ilsede")
    if _weather_cache["weather"] and (now - _weather_cache["timestamp"] < CACHE_TTL):
        return _weather_cache["weather"]
    try:
        resp = requests.get(WEATHER_API.format(location=location), timeout=5)
        if resp.status_code == 200:
            weather = resp.text.strip()
            _weather_cache["weather"] = weather
            _weather_cache["timestamp"] = now
            return weather
    except Exception:
        pass
    return "Weather unavailable"

@app.route('/')
def index():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    quote = get_quote()
    weather = get_weather()
    return render_template_string('''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Hermes Dashboard</title>
  <style>
    body { font-family: sans-serif; background:#111; color:#0f0; text-align:center; padding-top:10%; }
    .clock { font-size: 2rem; margin-bottom: 1rem; }
    .quote { font-size: 1.2rem; max-width: 600px; margin: auto; line-height: 1.5; }
    .weather { font-size: 1.2rem; max-width: 600px; margin: auto; line-height: 1.5; margin-top: 1rem; }
    a { color: #0ff; }
  </style>
</head>
<body>
  <div class="clock">{{ now }}</div>
  <div class="quote">{{ quote }}</div>
  <div class="weather">{{ weather }}</div>
</body>
</html>
''', now=now, quote=quote, weather=weather)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)