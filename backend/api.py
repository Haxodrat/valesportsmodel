# import statements
import requests
import random
import cloudscraper
from flask import Blueprint, jsonify

# blueprint for the API
api_bp = Blueprint('api_bp', __name__)

def get_upcoming_matches_data():
    """
    This endpoint fetches current (live score) Valorant esports match data
    from the unofficial vlr.gg API (vlrggapi).
    """
    # query param upcoming to fetch upcoming matches
    external_url = "http://vlrggapi.vercel.app/match?q=upcoming"
    
    # send a GET request to the vlrggapi endpoint
    # response = requests.get(external_url)
    # custom User-Agent header to mimic a browser
    # headers = {
    #     "User-Agent": "Mozilla/5.0"
    # }
    # Send a GET request to vlrggapi
    # response = requests.get(external_url, headers=headers)

    # use cloudscraper to bypass Cloudflare protection
    scraper = cloudscraper.create_scraper()
    response = scraper.get(external_url)  # No additional headers needed
    # Raise an exception for non-2xx status codes
    response.raise_for_status()

    # Parse the JSON data from the external API
    data = response.json()

    # extract match information:
    # { "data": { "status": 200, "segments": [ { match object }, ... ] } }
    matches = data.get("data", {}).get("segments", [])
    
    # build a list of simplified match objects
    simplified_matches = []

    # iterate through the matches
    for match in matches:
        # verify the required keys exist before processing
        if all(key in match for key in ["team1", "team2", "match_event", "match_page", "match_series", "time_until_match"]):
            # decide the predicted winner randomly (0.5 chance)
            predicted = random.choice([match["team1"], match["team2"]])
            
            simplified_matches.append({
                "match_event": match["match_event"],
                "match_page": match["match_page"],
                "match_series": match["match_series"],
                "predicted_winner": predicted,
                "teams": [match["team1"], match["team2"]],
                "time_until_match": match["time_until_match"]
            })
    
    return simplified_matches

# return the matches
@api_bp.route('/upcoming-matches', methods=['GET'])
def upcoming_matches():
    """
    This endpoint fetches current (live score) Valorant esports match data
    from the unofficial vlr.gg API (vlrggapi).
    """
    # call the function to get upcoming matches data
    try:
        matches = get_upcoming_matches_data()
        # return the modified data as json
        return jsonify({"data": matches}) 
    except requests.exceptions.RequestException as e:
        # Return an error message as JSON if any issues occur
        return jsonify({"error": str(e)}), 500