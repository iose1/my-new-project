from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

QUOTE_API = "https://api.quotable.io/random"

def get_quote():
    try:
        resp = requests.get(QUOTE_API, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return f"{data['content']} — {data['author']}"
    except Exception:
        pass
    return "Keep pushing forward. — Hermes"

@app.route('/')
def index():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    quote = get_quote()
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
    a { color: #0ff; }
  </style>
</head>
<body>
  <div class="clock">{{ now }}</div>
  <div class="quote">{{ quote }}</div>
</body>
</html>
''', now=now, quote=quote)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)