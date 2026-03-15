import React, { useState } from "react";

function App() {

  const [message, setMessage] = useState("");
  const [allData, setAllData] = useState([]);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!message.trim()) return;

    try {
      const res = await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: message
        })
      });

      const data = await res.json();

      console.log("Backend Response:", data);

      setAllData(prev => [...prev, data]);
      setMessage("");

    } catch (error) {
      console.log("Error:", error);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Interaction App</h1>

      <form onSubmit={sendMessage}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter message"
        />
        <button type="submit">Send</button>
      </form>

      <h2>All Messages</h2>

      <ul>
        {allData.map((item, index) => (
          <li key={index}>{item?.message}</li>
        ))}
      </ul>

    </div>
  );
}

export default App;