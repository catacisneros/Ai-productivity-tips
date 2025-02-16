from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 