from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
import wandb
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Weights & Biases (only once)
wandb.init(project="ai-productivity-tips")

# Load LlamaIndex from productivity_tips directory
def create_index():
    documents = SimpleDirectoryReader('./productivity_tips').load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.save_to_disk('index.json')
    return index

def query_index(question):
    # First get context from LlamaIndex
    index = VectorStoreIndex.load_from_disk('index.json')
    llama_response = index.query(question)
    
    # Then use Gemini to generate a more refined answer
    prompt = f"""
    Based on this context: {str(llama_response)}
    
    Please provide a detailed and helpful answer to this question: {question}
    
    Format your response in a clear, concise manner.
    """
    
    gemini_response = model.generate_content(prompt)
    final_response = gemini_response.text
    
    # Log both responses
    wandb.log({
        "question": question,
        "llama_response": str(llama_response),
        "gemini_response": final_response
    })
    
    return final_response

# Endpoint to handle queries from React frontend
@app.route('/query', methods=['POST'])
def query():
    question = request.json.get('question')
    try:
        response = query_index(question)
        return jsonify({"response": response, "error": None})
    except Exception as e:
        return jsonify({"response": None, "error": str(e)}), 500

if __name__ == '__main__':
    # Create index when the server starts
    index = create_index()
    app.run(debug=True)
