# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need
import random
import string
import re

def generate_short_code():
    """
    AI-assisted function:
    Generates a 6-character alphanumeric short code.
    Example: 'aB3xY7'
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def validate_url(url):
    """
    Validates that a URL starts with http:// or https://
    Returns True if valid, False otherwise.
    """
    pattern = r'^(http|https)://'
    return re.match(pattern, url) is not None
