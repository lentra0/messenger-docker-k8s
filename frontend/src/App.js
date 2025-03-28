import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [username, setUsername] = useState('');
  const socketRef = useRef(null);

  // Подключение к WebSocket
  useEffect(() => {
    if (!username) {
      const name = prompt('Введите ваше имя:') || 'Аноним';
      setUsername(name);
      return;
    }

    socketRef.current = new WebSocket(`ws://${window.location.hostname}:8000/ws/${username}`);

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'history') {
        setMessages(data.data.reverse());
      }
      else if (data.type === 'message') {
        setMessages(prev => [data.data, ...prev]);
      }
    };

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [username]);

  const sendMessage = () => {
    if (input.trim() && socketRef.current) {
      socketRef.current.send(input);
      setInput('');
    }
  };

  return (
    <div className="app">
    <header className="app-header">
    <h1>Чат ({username})</h1>
    </header>

    <div className="messages-container">
    {messages.map((msg, i) => (
      <div key={i} className="message">
      <span className="user">{msg.user}: </span>
      <span className="text">{msg.text}</span>
      <span className="time">
      {new Date(msg.time).toLocaleTimeString()}
      </span>
      </div>
    ))}
    </div>

    <div className="input-area">
    <input
    type="text"
    value={input}
    onChange={(e) => setInput(e.target.value)}
    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
    placeholder="Введите сообщение..."
    />
    <button onClick={sendMessage}>Отправить</button>
    </div>
    </div>
  );
}

export default App;
