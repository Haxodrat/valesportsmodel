# imports
import os
from flask import Blueprint, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create a blueprint for our API endpoints
api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/valorant-data', methods=['GET'])
def get_valorant_data():
    # Retrieve the API key from environment variables
    api_key = os.getenv('PANDASCORE_API_KEY')
    if not api_key:
        return jsonify({'error': 'PandaScore API key not set'}), 500

    # endpoint URL for fetching Valorant matches without query parameter in url
    external_url = "https://api.pandascore.co/valorant/matches"
    
    # bearer token auth
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(external_url, headers=headers)
        # Raises an error for non-2XX responses
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
