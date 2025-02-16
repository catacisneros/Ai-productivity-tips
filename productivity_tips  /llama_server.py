from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
import wandb
from flask import Flask, request, jsonify
from flask_cors import CORS

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
    index = VectorStoreIndex.load_from_disk('index.json')
    response = index.query(question)
    wandb.log({"question": question, "response": str(response)})
    return response

# Endpoint to handle queries from React frontend
@app.route('/query', methods=['POST'])
def query():
    question = request.json.get('question')
    response = query_index(question)
    return jsonify({"response": str(response)})

if __name__ == '__main__':
    # Create index when the server starts
    index = create_index()
    app.run(debug=True)
