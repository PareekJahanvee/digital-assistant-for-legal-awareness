from flask import Flask, request, jsonify
from flask_cors import CORS

from chatbot1 import get_best_answer

app = Flask(__name__)
CORS(app)  #  Important for React connection

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"response": "Please enter a valid question."})

        #  Call chatbot logic
        bot_response = get_best_answer(user_message)

        return jsonify({
            "response": bot_response
        })

    except Exception as e:
        return jsonify({
            "response": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True, port=5000)