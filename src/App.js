import React, { useState } from 'react';

import './App.css';

function App() {
  // State to manage user input and backend response
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Function to query the Flask backend
  const queryproductivity_tips = async () => {
    setIsLoading(true);
    try {
      const res = await fetch('http://localhost:5001/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message }), // Send the message to the backend
      });

      const data = await res.json();
      setResponse(data.response); // Store the backend response
    } catch (error) {
      console.error('Error:', error);
      setResponse('Oops! Something went wrong. Please try again!');
    }
    setIsLoading(false);
  };

  return (
    <div className="app-container">
      <h1 className="header">AI Productivity Tips</h1>
      
      <div className="input-section">
        <input
          className="input-field"
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)} // Update the message state
          placeholder="Ask me anything about productivity! 💭"
        />
        <button 
          className="submit-button"
          onClick={queryproductivity_tips}
          disabled={isLoading}
        >
          {isLoading ? "Thinking..." : "Ask! ✨"}
        </button>
      </div>

      <div className="response-section">
        <h2 className="response-header">Response</h2>
        <p className={`response-text ${isLoading ? 'loading' : ''}`}>
          {isLoading ? "Thinking" : response || "Ask me something! I'm here to help! 🌟"}
        </p>
      </div>
    </div>
  );
}

export default App;
