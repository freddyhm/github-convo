from flask import Flask, render_template, request, jsonify
from third_parties.github import get_github_data, generate_conversation_starters
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_github():
    data = request.json
    username = data.get("username")
    try:
        conversation_starters = generate_conversation_starters(username)
        
        print("Debug - API Response:", {
            "profile": conversation_starters["profile"],
            "contributions": conversation_starters["contributions"],
            "conversation_starters": conversation_starters
        })
        
        return jsonify({
            "profile": conversation_starters["profile"],
            "contributions": conversation_starters["contributions"],
            "conversation_starters": conversation_starters
        })
    except Exception as error:
        print(f"Debug - Error: {str(error)}")
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
