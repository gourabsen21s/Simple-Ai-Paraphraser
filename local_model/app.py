from flask import Flask, request, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
def paraphrase_text(input_text):
    input_text = "paraphrase: " + input_text + " </s>"
    encoding = tokenizer.encode_plus(input_text, return_tensors="pt", padding=True)
    output = model.generate(
        input_ids=encoding['input_ids'],
        max_length=256,
        num_beams=5,
        no_repeat_ngram_size=2,
        num_return_sequences=1,
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
    app.run(host='0.0.0.0', port=5000)
