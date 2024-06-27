from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

script_path = "./book-recommender.py"


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(force=True)
    isbn = data.get("isbn", "")
    bookName = data.get("bookName", "")
    number = data.get("number", "")
    place = data.get("place", "")

    result = subprocess.run(
        ["python3", script_path, isbn, bookName, str(number), place],
        capture_output=True,
        text=True,
    )

    if result.stderr:
        app.logger.error(f"Error from script: {result.stderr}")
        return jsonify(
            {"error": "Error in script execution", "details": result.stderr}
        ), 500

    try:
        recommendations = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        app.logger.error(f"JSON decoding failed: {e} - Output: {result.stdout}")
        return jsonify({"error": "Invalid JSON output from script"}), 500
    print("recommendations", recommendations)
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
