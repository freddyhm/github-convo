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
        github_data = get_github_data(username)
        conversation_starters = generate_conversation_starters(github_data)
        
        print("Debug - API Response:", {
            "profile": github_data["profile"],
            "contributions": github_data["contributions"],
            "conversation_starters": conversation_starters
        })
        
        return jsonify({
            "profile": github_data["profile"],
            "contributions": github_data["contributions"],
            "conversation_starters": conversation_starters
        })
    except Exception as error:
        print(f"Debug - Error: {str(error)}")
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
