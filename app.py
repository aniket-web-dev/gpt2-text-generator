from flask import Flask, request, render_template_string
from generator import GPT2TextGenerator

app = Flask(__name__)
generator = GPT2TextGenerator()

# Basic HTML for form interface
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>GPT-2 Text Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f8;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            color: #333;
        }
        .container {
            background: white;
            max-width: 700px;
            width: 90%;
            margin: 40px 0;
            padding: 30px 40px;
            border-radius: 8px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 25px;
            font-weight: 700;
        }
        label {
            font-weight: 600;
            display: block;
            margin-bottom: 8px;
            color: #34495e;
        }
        textarea {
            width: 100%;
            height: 120px;
            padding: 12px 15px;
            font-size: 1rem;
            border: 1px solid #ccc;
            border-radius: 5px;
            resize: vertical;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        textarea:focus {
            border-color: #2980b9;
            outline: none;
        }
        input[type="number"] {
            width: 100px;
            padding: 8px 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        input[type="number"]:focus {
            border-color: #2980b9;
            outline: none;
        }
        .form-row {
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        button {
            display: block;
            width: 100%;
            background-color: #2980b9;
            color: white;
            padding: 14px;
            font-size: 1.1rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 700;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #1c5980;
        }
        hr {
            margin: 30px 0;
            border: none;
            border-top: 1px solid #e1e4e8;
        }
        h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-weight: 700;
        }
        pre {
            background-color: #eeeeee;
            padding: 20px;
            border-radius: 6px;
            white-space: pre-wrap;
            font-family: 'Courier New', Courier, monospace;
            font-size: 1rem;
            color: #2c3e50;
            max-height: 400px;
            overflow-y: auto;
        }
        @media (max-width: 480px) {
            .form-row {
                flex-direction: column;
                align-items: stretch;
            }
            input[type="number"] {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GPT-2 Text Generator</h1>
        <form method="POST">
            <div class="form-row">
                <label for="prompt">Enter prompt text:</label>
                <textarea id="prompt" name="prompt" placeholder="Type your prompt here...">{{prompt}}</textarea>
            </div>
            <div class="form-row" style="align-items:center;">
                <label for="max_length">Max length:</label>
                <input type="number" id="max_length" name="max_length" value="{{max_length}}" min="10" max="300" />
            </div>
            <button type="submit">Generate Text</button>
        </form>
        <hr />
        {% if result %}
        <h3>Generated Text:</h3>
        <pre>{{result}}</pre>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    prompt = ""
    max_length = 100
    if request.method == 'POST':
        prompt = request.form.get("prompt", "")
        max_length = int(request.form.get("max_length", 100))
        result_list = generator.generate_text(prompt, max_length=max_length, num_return_sequences=1)
        result = result_list[0] if result_list else "No output generated."
    return render_template_string(HTML_TEMPLATE, result=result, prompt=prompt, max_length=max_length)

if __name__ == '__main__':
    app.run(debug=True)
