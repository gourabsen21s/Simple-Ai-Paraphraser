from flask import Flask, request, jsonify
from transformers import GPT2Tokenizer, GPT2LMHeadModel

app = Flask(__name__)

# Use DistilGPT-2 instead of GPT-Neo
model_name = "distilgpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set the pad_token_id to eos_token_id to avoid warnings
tokenizer.pad_token_id = tokenizer.eos_token_id

def paraphrase_text(input_text):
    # Tokenize input text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    
    # Generate text with faster and smaller model
    output = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=150,  # Limit max length for speed
        num_beams=3,  # Reduce the number of beams for faster generation
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    paraphrased_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return paraphrased_text

@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    data = request.get_json()
    input_text = data['text']
    paraphrased_output = paraphrase_text(input_text)
    return jsonify({'paraphrasedText': paraphrased_output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
