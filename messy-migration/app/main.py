from flask import Flask
from app.routes import bp
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

app = create_app()

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
