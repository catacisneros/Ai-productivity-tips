import React, { useState } from 'react';

function App() {
  // State to manage user input and backend response
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  // Function to query the Flask backend
  const queryproductivity_tips = async () => {
    const res = await fetch('http://localhost:5001/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: message }), // Send the message to the backend
    });

    const data = await res.json();
    setResponse(data.response); // Store the backend response
  };

  return (
    <div>
      <h1>AI Productivity Tips</h1>
      {/* Input field for the user's question */}
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)} // Update the message state
        placeholder="Ask a productivity tip..."
      />
      <button onClick={queryproductivity_tips}>Submit</button>

      {/* Display the response from the backend */}
      <div>
        <h2>Response:</h2>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
