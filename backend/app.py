# backend/app.py

from flask import Flask
from flask_cors import CORS

from api import api_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(api_bp)

    @app.route("/")
    def healthcheck():
        return {"status": "ok", "message": "Valorant Esports Model backend is running"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)