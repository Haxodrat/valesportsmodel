from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Chris is working'})

# A dummy /predict endpoint
@app.route('/predict')
def predict():
    # In the future, you'll replace these static values with prediction logic.
    return jsonify(teamA_win_probability=0.65, teamB_win_probability=0.35)

if __name__ == '__main__':
    app.run(debug=True)