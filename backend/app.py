# imports
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from api import api_bp, get_upcoming_matches_data

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='../frontend')

# home page
@app.route('/')
def home():
    return jsonify(message="Backend is up and running!")

# register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

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
