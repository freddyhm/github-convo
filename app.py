from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from conversation_starters import generate_conversation_starters
from output_parsers import github_data_parser
from openai import OpenAI
from agents.github_agent import create_github_agent


load_dotenv()

app = Flask(__name__)

def create_inputs(username: str):
    prompt = f"""Given the username {username}, retrieve their Github data and return it in the following JSON format without any markdown formatting or code blocks. The output should be a raw JSON object.

                 { github_data_parser.get_format_instructions() }

                 Remember: Return ONLY the JSON object without any additional text, markdown formatting, or code blocks."""

    return {"messages": [("user", prompt)]}

def get_github_info(raw_output: str):
    parsed_data = github_data_parser.parse(raw_output)
    github_info = generate_conversation_starters(parsed_data)

    return {
        "profile": github_info["profile"],
        "contributions": github_info["contributions"],
        "conversation_starters": github_info
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_github():
    data = request.json
    username = data.get("username")

    try:

        inputs = create_inputs(username)
        message = create_github_agent(inputs.get("messages")[0][1])
        result = get_github_info(raw_output=message)

        return result

    except Exception as error:
        print(f"Debug - Error: {str(error)}")
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)