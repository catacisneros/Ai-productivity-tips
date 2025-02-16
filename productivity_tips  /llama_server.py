from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure API keys from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not GOOGLE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Missing API keys in .env file")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = """You are a productivity expert. Provide helpful, practical advice about productivity, time management, and efficiency. 
Focus on actionable tips and real-world examples. Base your answers on well-known productivity principles and methodologies."""

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        question = data.get('question', '')
        if not question:
            return jsonify({'response': 'Please ask a question!'}), 400

        # Get responses from both models
        try:
            # Gemini response
            gemini_response = gemini_model.generate_content(
                f"As a productivity expert, answer this question: {question}"
            )
            gemini_answer = gemini_response.text
        except Exception as e:
            print(f"Gemini Error: {str(e)}")
            gemini_answer = None

        try:
            # OpenAI response
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ]
            )
            openai_answer = openai_response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {str(e)}")
            openai_answer = None

        # Use whichever response is available, preferring OpenAI if both are available
        if openai_answer:
            final_response = openai_answer
        elif gemini_answer:
            final_response = gemini_answer
        else:
            return jsonify({'response': 'Sorry, both AI services are currently unavailable.'}), 500

        return jsonify({'response': final_response})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
