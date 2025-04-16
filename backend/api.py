# import statements
import requests
from flask import Blueprint, jsonify

# blueprint for the API
api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/valorant-current', methods=['GET'])
def get_valorant_current():
    """
    This endpoint fetches current (live score) Valorant esports match data
    from the unofficial vlr.gg API (vlrggapi).
    """
    # query param upcoming to fetch upcoming matches
    external_url = "https://vlrggapi.vercel.app/match?q=upcoming"
    
    try:
        # send a GET request to the vlrggapi endpoint
        response = requests.get(external_url)
        # Raise an exception for non-2xx status codes
        response.raise_for_status()

        # Parse the JSON data from the external API
        data = response.json()
        return jsonify(data)
    
    except requests.exceptions.RequestException as e:
        # Return an error message as JSON if any issues occur
        return jsonify({"error": str(e)}), 500
