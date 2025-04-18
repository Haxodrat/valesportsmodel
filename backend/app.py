# imports
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from api import api_bp, get_upcoming_matches_data, fetch_news_data, fetch_past_matches_data, fetch_live_matches_data

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='../front')
CORS(app)

# home page
@app.route('/')
def home():
    return jsonify(message="Backend is up and running!")

# register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# news page
@app.route('/news', methods=['GET'])
def news_page():
    """
    This route uses the helper function from your API blueprint to get valo news.
    """
    try:
        news = fetch_news_data()
        # catches iterable object
        if not hasattr(news, '__iter__'):
            raise TypeError("Returned news data is not iterable")
        # render html template with news data
        return render_template('news.html', news=news)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# # stats page
# @app.route('/stats', methods=['GET'])
# def stats_page():
#     """
#     Render player stats, filtered by region & (optionally) tournament.
#     Query params:
#       - region: default 'na'
#       - tournament: optional, will filter on stat['tournament_name']
#     """
#     region     = request.args.get('region', 'na')
#     tournament = request.args.get('tournament')  # e.g. 'Champions Tour 2024: Americas Stage 1'

#     try:
#         # 1) fetch all stats
#         all_stats = fetch_stats_data(region=region, timespan='all')

#         # 2) if tournament filter is set, figure out which teams play in that event:
#         if tournament:
#             upcoming = get_upcoming_matches_data()
#             teams_in_event = {
#                 team
#                 for m in upcoming
#                 if m['match_event'] == tournament
#                 for team in m['teams']
#             }
#             # 3) filter stats by org in that team set
#             all_stats = [s for s in all_stats if s.get('org') in teams_in_event]

#         return render_template(
#             'stats.html',
#             stats=all_stats,
#             region=region,
#             tournament=tournament
#         )
#     # """
#     # This route uses the helper function from your API blueprint to get player stats.
#     # """
#     # try:
#     #     stats = fetch_stats_data(region='na', timespan='all')
#     #     # catches iterable object
#     #     if not hasattr(stats, '__iter__'):
#     #         raise TypeError("Returned stats data is not iterable")
#     #     # render html template with stats data
#     #     return render_template('stats.html', stats=stats)
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# # rankings page
# @app.route('/rankings', methods=['GET'])
# def rankings_page():
#     """
#     Render team rankings, filtered by region & (optionally) tournament.
#     Query params:
#       - region: default 'na'
#       - tournament: optional, will filter on ranking['tournament_name']
#     """
#     region     = request.args.get('region', 'na')
#     tournament = request.args.get('tournament')

#     try:
#         # 1) fetch all rankings
#         all_rankings = fetch_rankings_data(region=region)

#         # 2) if tournament filter is set, find participating teams
#         if tournament:
#             upcoming = get_upcoming_matches_data()
#             teams_in_event = {
#                 team
#                 for m in upcoming
#                 if m['match_event'] == tournament
#                 for team in m['teams']
#             }
#             # 3) filter rankings by team in that set
#             all_rankings = [r for r in all_rankings if r.get('team') in teams_in_event]

#         return render_template(
#             'rankings.html',
#             rankings=all_rankings,
#             region=region,
#             tournament=tournament
#         )
    # """
    # This route uses the helper function from your API blueprint to get team rankings.
    # """
    # try:
    #     rankings = fetch_rankings_data(region='na')
    #     # catches iterable object
    #     if not hasattr(rankings, '__iter__'):
    #         raise TypeError("Returned rankings data is not iterable")
    #     # render html template with rankings data
    #     return render_template('rankings.html', rankings=rankings)
    
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

# matches page
@app.route('/matches', methods=['GET'])
def matches_page():
    """
    This route uses the helper function from your API blueprint to get upcoming matches,
    then renders an HTML page displaying the match event, series, teams, time until match,
    and the predicted winner.
    """
    try:
        matches = get_upcoming_matches_data()
        # catches iterable object
        if not hasattr(matches, '__iter__'):
            raise TypeError("Returned matches data is not iterable")
        # render html template with matches data
        return render_template('matches.html', matches=matches)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# past matches page
@app.route('/past-matches', methods=['GET'])
def past_matches_page():
    """
    This route uses the helper function from your API blueprint to get past matches,
    then renders an HTML page displaying the match event, series, teams, scores, time completed,
    and the match page.
    """
    try:
        past = fetch_past_matches_data()
        # catches iterable object
        if not hasattr(past, '__iter__'):
            raise TypeError("Returned past matches data is not iterable")
        # render html template with matches data
        return render_template('past-matches.html', past=past)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# live matches page
@app.route('/live-matches', methods=['GET'])
def live_matches_page():
    """
    This route uses the helper function from your API blueprint to get live matches,
    then renders an HTML page displaying the match event, series, teams, scores, time started,
    and the match page.
    """
    try:
        live = fetch_live_matches_data()
        # catches iterable object
        if not hasattr(live, '__iter__'):
            raise TypeError("Returned live matches data is not iterable")
        # render html template with matches data
        return render_template('live-matches.html', live=live)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
