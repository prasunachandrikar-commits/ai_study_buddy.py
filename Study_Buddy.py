from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>AI Study Buddy 💬</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background: #f3f4f6;
          margin: 0; padding: 0;
          display: flex; flex-direction: column;
          align-items: center; height: 100vh;
        }
        h1 { margin-top: 20px; color: #333; }
        #chat-box {
          width: 90%; max-width: 600px;
          height: 70vh; background: white;
          border-radius: 10px; padding: 15px;
          overflow-y: scroll; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .user, .bot {
          margin: 10px 0; padding: 10px;
          border-radius: 10px; max-width: 80%;
        }
        .user { background: #d1e7dd; align-self: flex-end; }
        .bot { background: #f8d7da; align-self: flex-start; }
        #input-area {
          width: 90%; max-width: 600px;
          display: flex; margin-top: 10px;
        }
        input {
          flex: 1; padding: 10px; border-radius: 5px;
          border: 1px solid #ccc;
        }
        button {
          padding: 10px 15px; border: none;
          background: #007bff; color: white;
          border-radius: 5px; margin-left: 10px;
          cursor: pointer;
        }
        button:hover { background: #0056b3; }
      </style>
    </head>
    <body>
      <h1>🤖 AI Study Buddy (Offline + Quiz)</h1>
      <div id="chat-box"></div>

      <div id="input-area">
        <input id="user-input" type="text" placeholder="Ask something...">
        <button onclick="sendMessage()">Send</button>
      </div>

      <script>
        async function sendMessage() {
          const input = document.getElementById("user-input");
          const message = input.value.trim();
          if (!message) return;
          
          const chatBox = document.getElementById("chat-box");
          chatBox.innerHTML += `<div class='user'>You: ${message}</div>`;
          input.value = "";

          const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
          });
          const data = await response.json();

          chatBox.innerHTML += `<div class='bot'>Buddy: ${data.reply}</div>`;
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      </script>
    </body>
    </html>
    '''

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"].lower()

    topics = {
        "python": {
            "info": "🐍 Python is a versatile programming language known for its readability and simplicity.",
            "quiz": [
                ("What keyword is used to define a function in Python?", "def"),
                ("Which data type is mutable: tuple or list?", "list"),
                ("What symbol is used for comments?", "#")
            ]
        },
        "dbms": {
            "info": "🗄️ DBMS (Database Management System) helps manage and organize large sets of data efficiently.",
            "quiz": [
                ("What does DBMS stand for?", "database management system"),
                ("Which language is used to query databases?", "sql"),
                ("What is a primary key?", "unique identifier for records")
            ]
        },
        "ai": {
            "info": "🤖 AI (Artificial Intelligence) enables machines to mimic human intelligence and decision-making.",
            "quiz": [
                ("What does AI stand for?", "artificial intelligence"),
                ("Name one application of AI.", "chatbot"),
                ("AI is part of which field of study?", "computer science")
            ]
        },
        "trigonometry": {
            "info": "📐 Trigonometry deals with angles and sides of triangles. Example: sinθ = opposite/hypotenuse.",
            "quiz": [
                ("What is sin 90°?", "1"),
                ("What is tan 45°?", "1"),
                ("What is the formula for cosθ?", "adjacent/hypotenuse")
            ]
        },
        "machine learning": {
            "info": "🤖 Machine Learning allows computers to learn from data without explicit programming.",
            "quiz": [
                ("What does ML stand for?", "machine learning"),
                ("Which algorithm is used for classification?", "logistic regression"),
                ("What is the main goal of ML?", "to learn patterns from data")
            ]
        }
    }

    # Default response
    reply = "I'm not sure about that topic yet. Try asking about Python, DBMS, AI, Trigonometry, or Machine Learning."

    for topic, data in topics.items():
        if topic in user_message:
            reply = data["info"] + "<br><br><b>📝 Quiz Time!</b><br>"
            for i, (q, _) in enumerate(data["quiz"], start=1):
                reply += f"{i}. {q}<br>"
            reply += "<br>Type your answers here! 😊"
            break

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
