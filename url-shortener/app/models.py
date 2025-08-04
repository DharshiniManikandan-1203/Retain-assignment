from datetime import datetime

# In-memory storage for shortened URLs
# Structure:
# {
#    "abc123": {
#        "url": "https://example.com",
#        "clicks": 0,
#        "created_at": datetime.utcnow()
#    }
# }
url_store = {}

def add_url(short_code, original_url):
    """Add a new URL mapping to the store"""
    url_store[short_code] = {
        "url": original_url,
        "clicks": 0,
        "created_at": datetime.utcnow()
    }

def get_url(short_code):
    """Retrieve URL data for a given short code"""
    return url_store.get(short_code)

def increment_click(short_code):
    """Increment click count for a given short code"""
    if short_code in url_store:
        url_store[short_code]["clicks"] += 1
