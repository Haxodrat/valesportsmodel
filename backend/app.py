# imports
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from api import api_bp, get_upcoming_matches_data, fetch_news_data, fetch_rankings_data, fetch_stats_data

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
    
# stats page
@app.route('/stats', methods=['GET'])
def stats_page():
    """
    This route uses the helper function from your API blueprint to get player stats.
    """
    try:
        stats = fetch_stats_data(region='na', timespan='all')
        # catches iterable object
        if not hasattr(stats, '__iter__'):
            raise TypeError("Returned stats data is not iterable")
        # render html template with stats data
        return render_template('stats.html', stats=stats)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# rankings page
@app.route('/rankings', methods=['GET'])
def rankings_page():
    """
    This route uses the helper function from your API blueprint to get team rankings.
    """
    try:
        rankings = fetch_rankings_data(region='na')
        # catches iterable object
        if not hasattr(rankings, '__iter__'):
            raise TypeError("Returned rankings data is not iterable")
        # render html template with rankings data
        return render_template('rankings.html', rankings=rankings)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
