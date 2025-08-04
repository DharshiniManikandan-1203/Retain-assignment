from flask import Flask, jsonify, request, redirect
from datetime import datetime
from app.models import url_store, add_url, get_url, increment_click
from app.utils import generate_short_code, validate_url

app = Flask(__name__)


@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })
    
# New URL Shortener Endpoints


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """Accepts a long URL and returns a short URL with 6-char code"""
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400

    original_url = data["url"]
    if not validate_url(original_url):
        return jsonify({"error": "Invalid URL format"}), 400

    short_code = generate_short_code()
    add_url(short_code, original_url)
    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({"short_code": short_code, "short_url": short_url}), 200


@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    """Redirects to original URL and increments click count"""
    url_data = get_url(short_code)
    if not url_data:
        return jsonify({"error": "Short code not found"}), 404

    increment_click(short_code)
    return redirect(url_data["url"], code=302)


@app.route("/api/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    """Returns analytics: original URL, click count, and creation timestamp"""
    url_data = get_url(short_code)
    if not url_data:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": url_data["url"],
        "clicks": url_data["clicks"],
        "created_at": url_data["created_at"].isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


