
import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement> | React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    try {
      console.log("Sending question: ", question);
      const response = await fetch('http://localhost:8000/prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });
      const data = await response.text();
      console.log('Agent response:', data);
    } catch (error) {
      console.error('Error fetching response:', error);
    } finally {
      setLoading(false);
      setQuestion('');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: '#f5f5f5' }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem', background: '#fff', padding: '2rem', borderRadius: '12px', boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
        <h2 style={{ marginBottom: '1rem' }}>Physics Agent Chat</h2>
        <input
          type="text"
          value={question}
          onChange={handleInputChange}
          placeholder="Type your physics question..."
          style={{ width: '320px', padding: '0.75rem', fontSize: '1rem', borderRadius: '8px', border: '1px solid #ccc' }}
          disabled={loading}
        />
        <button
          type="submit"
          onClick={handleSubmit}
          style={{ padding: '0.75rem 2rem', fontSize: '1rem', borderRadius: '8px', background: '#007bff', color: '#fff', border: 'none', cursor: 'pointer' }}
          disabled={loading}
        >
          {loading ? 'Waiting...' : 'Ask'}
        </button>
      </form>
    </div>
  );
}

export default App;
