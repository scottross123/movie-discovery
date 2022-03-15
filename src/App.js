import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

function App() {

  const [currentFact, setCurrentFact] = useState("");

  function handleClick () {
    console.log("zendaya")
      fetch("/facts", {
        method:"POST",
        cache: "no-cache",
        headers:{
            "content_type":"application/json",
        },
        body: JSON.stringify(currentFact)
        }
    ).then(response => {
    return response.json()
    })
    .then(json => {
    setCurrentFact(json)
    })
  }

  
  return (
    <div className="App">
      <p>{currentFact}</p>
      <button onClick={handleClick}>
        Learn a fun fact!!!
      </button>
    </div>
  );
}

export default App;
