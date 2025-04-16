# imports
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from api import api_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)

# home page
@app.route('/')
def home():
    return jsonify(message="Backend is up and running!")

# register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)