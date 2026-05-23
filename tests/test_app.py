import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import app

def test_app_exists():
    assert app is not None

def test_quote_caching():
    # Just ensure the function exists
    from app import get_quote
    assert callable(get_quote)