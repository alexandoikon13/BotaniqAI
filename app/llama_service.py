from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

model_name = "EleutherAI/gpt-neo-125M"  # Example model, choose as per your requirement
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    inputs = tokenizer.encode(data['text'], return_tensors='pt')
    outputs = model.generate(inputs, max_length=50)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'generated_text': text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
