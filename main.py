from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'SoulChat BaZi API is live!'

@app.route('/bazi', methods=['POST'])
def bazi():
    data = request.get_json()
    name = data.get("name", "Unknown")
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")
    hour = data.get("hour")

    # Placeholder logic – replace with actual BaZi analysis later
    personality = "Sensitive, thoughtful, and detail-oriented."
    luck = "This year brings opportunities for personal growth and connection."
    
    return jsonify({
        "status": "success",
        "name": name,
        "personality": personality,
        "luck": luck
    })
