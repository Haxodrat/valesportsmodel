# import statements
import requests
import random
import cloudscraper
from flask import Blueprint, jsonify, request

# blueprint for the API
api_bp = Blueprint('api_bp', __name__)

# getting news
def fetch_news_data() -> list:
    """
    Fetches the latest Valorant esports news articles.
    Returns a list of news segments.
    """
    url = "https://vlrggapi.vercel.app/news"
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    resp.raise_for_status()
    data = resp.json()
    # structure: { "data": { "status": 200, "segments": [...] } }
    return data.get("data", {}).get("segments", [])

@api_bp.route('/news', methods=['GET'])
def news():
    """API endpoint to return the latest news as JSON."""
    try:
        segments = fetch_news_data()
        return jsonify({"data": segments})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# getting stats
def fetch_stats_data(region: str = "na", timespan: str = "all") -> list:
    """
    Fetches player statistics for a given region and timespan.
    Returns a list of stat segments.
    """
    url = f"https://vlrggapi.vercel.app/stats?region={region}&timespan={timespan}"
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    resp.raise_for_status()
    data = resp.json()
    # structure: { "data": { "status": 200, "segments": [...] } }
    return data.get("data", {}).get("segments", [])

@api_bp.route('/stats', methods=['GET'])
def stats():
    """
    API endpoint to return player stats.
    Query params:
      - region: e.g. 'na', 'eu', etc. (default 'na')
      - timespan: days (e.g. '30') or 'all' (default '30')
    """
    try:
        region = request.args.get("region", "na")
        timespan = request.args.get("timespan", "30")
        segments = fetch_stats_data(region, timespan)
        return jsonify({"data": segments})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# getting the rankings data
def fetch_rankings_data(region: str = "na") -> list:
    """
    Fetches team rankings for a given region.
    Returns a list of ranking entries.
    """
    url = f"https://vlrggapi.vercel.app/rankings?region={region}"
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    resp.raise_for_status()
    data = resp.json()
    # structure: { "status": 200, "data": [...] }
    return data.get("data", [])

@api_bp.route('/rankings', methods=['GET'])
def rankings():
    """
    API endpoint to return team rankings.
    Query params:
      - region: e.g. 'na', 'eu', etc. (default 'na')
    """
    try:
        region = request.args.get("region", "na")
        entries = fetch_rankings_data(region)
        return jsonify({"data": entries})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

# gets past matches
def fetch_past_matches_data() -> list[dict]:
    """
    Fetches all completed Valorant matches from the unofficial vlr.gg API.
    Returns a list of match dicts normalized to include:
      - tournament_name (as match_event)
      - teams (a list of the two teams)
      - round_info (as match_series)
      - match_page
      - time_completed (as time_until_match)
    """
    url = "https://vlrggapi.vercel.app/match?q=results"
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    resp.raise_for_status()
    data = resp.json().get("data", {}).get("segments", [])
    # Normalize each segment into your Matches shape
    normalized = []

    # iterate through the segments
    for seg in data:
        normalized.append({
            "match_event": seg.get("tournament_name", "Unknown Event"),
            "teams": [seg.get("team1"), seg.get("team2")],
            "match_series": seg.get("round_info", ""),
            "match_page": seg.get("match_page", ""),
            "predicted_winner": None,
            "time_until_match": seg.get("time_completed", "")
        })
    return normalized

@api_bp.route('/past-matches', methods=['GET'])
def past_matches():
    try:
        matches = fetch_past_matches_data()
        return jsonify({ "data": matches })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500