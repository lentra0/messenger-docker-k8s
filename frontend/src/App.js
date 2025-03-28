import React, { useState, useEffect } from 'react';
function App() {
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const ws = new WebSocket('ws://localhost:8000/ws/user1');

    useEffect(() => {
        ws.onmessage = (event) => {
            setMessages(prev => [...prev, JSON.parse(event.data)]);
        };
    }, []);

    const sendMessage = () => {
        ws.send(message);
        setMessage('');
    };

    return (
        <div>
        <div>
        {messages.map((msg, i) => (
            <p key={i}>{msg.user}: {msg.text}</p>
        ))}
        </div>
        <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage}>Отправить</button>
        </div>
    );
}
export default App;
