# backend/app.py

from flask import Flask
from flask_cors import CORS

from api import api_bp
from configs.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    allowed_origins = [
        app.config["FRONTEND_URL"],
        "http://localhost:3000",
    ]

    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    app.register_blueprint(api_bp)

    @app.route("/")
    def healthcheck():
        return {
            "status": "ok",
            "message": "Valorant Esports Model backend is running",
            "vlr_api_base_url": app.config["VLR_API_BASE_URL"],
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])