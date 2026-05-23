import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import app, get_quote, get_weather, _quote_cache, _weather_cache, CACHE_TTL
import time
from unittest.mock import patch, Mock

def test_app_exists():
    assert app is not None

def test_quote_caching():
    # Just ensure the function exists
    assert callable(get_quote)

def test_weather_caching():
    assert callable(get_weather)

def test_index_route():
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        # Check for expected elements
        assert '<div class="clock">' in html
        assert '<div class="quote">' in html
        assert 'Wetter in Ilsede:' in html

@patch('app.requests.get')
def test_quote_cache_ttl(mock_get):
    # Mock the API response
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        'content': 'Test quote content',
        'author': 'Test Author'
    }
    mock_get.return_value = mock_resp

    # Set cache to expired
    now = time.time()
    _quote_cache['quote'] = 'old quote'
    _quote_cache['timestamp'] = now - (CACHE_TTL + 1)  # expired

    # Call get_quote, should use the mocked API and update cache
    quote = get_quote()
    assert isinstance(quote, str)
    assert quote == 'Test quote content — Test Author'
    # Cache should be updated
    assert _quote_cache['quote'] == quote
    assert _quote_cache['timestamp'] >= now - 1  # allow small drift

@patch('app.requests.get')
def test_weather_cache_ttl(mock_get):
    # Mock the API response
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        'current_weather': {
            'temperature': 20.0,
            'windspeed': 10.0
        }
    }
    mock_get.return_value = mock_resp

    # Set cache to expired
    now = time.time()
    _weather_cache['weather'] = 'old weather'
    _weather_cache['timestamp'] = now - (CACHE_TTL + 1)  # expired

    # Call get_weather, should use the mocked API and update cache
    weather = get_weather()
    assert isinstance(weather, str)
    assert '20.0°C' in weather
    # Cache should be updated
    assert _weather_cache['weather'] == weather
    assert _weather_cache['timestamp'] >= now - 1

def test_api_route():
    with app.test_client() as client:
        resp = client.get('/api')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'time' in data
        assert 'quote' in data
        assert 'weather' in data
        # Check that quote and weather are strings
        assert isinstance(data['quote'], str)
        assert isinstance(data['weather'], str)