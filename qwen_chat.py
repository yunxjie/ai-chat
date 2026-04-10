from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify, render_template
import torch

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-0.5B-Chat")

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen1.5-0.5B-Chat",
    torch_dtype="auto",
    device_map="auto"
)

history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global history

    user_input = request.json["message"]

    history.append(f"用户：{user_input}")

    if len(history) > 10:
        history = history[-10:]

    prompt = "你是一个中文助手，只回答用户问题，不要重复用户的话。\n" + "\n".join(history) + "\nAI："

    messages = [
    {"role": "system", "content": "你是一个中文助手"},
    {"role": "user", "content": user_input}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200
    )

    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)

# 截断异常内容
    stop_words = ["用户：", "AI：", "User:", "Assistant:", "\n用户", "\nAI"]

    for stop_word in stop_words:
        if stop_word in reply:
            reply = reply.split(stop_word)[0]

    reply = reply.split("assistant")[-1].strip()

# 限制长度（防止胡言乱语）
    reply = reply[:200]

# 防空回复
    if not reply:
        reply = "我暂时不知道怎么回答这个问题 🤔"
    
# 加入历史（非常重要）
    history.append(f"AI：{reply}")

    return jsonify({"reply": reply})
    
if __name__ == "__main__":
    app.run(debug=True)
