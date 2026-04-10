import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
print("API_KEY =", API_KEY)

def call_qwen(user_input):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print("返回数据：", result)

    if "output" in result:
        return result["output"]["choices"][0]["message"]["content"]
    else:
        return str(result)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]
        reply = call_qwen(user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        print("错误：", e)
        return jsonify({"reply": "服务器出错了"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
