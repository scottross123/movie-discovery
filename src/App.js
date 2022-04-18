import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import {Rating} from './Rating.js';

function App() {

  const [ratings, setRatings] = useState([]);

  function handleDelete(i) {
    setRatings([...ratings.slice(0, i), ...ratings.slice(i+1)]);
  }

  function handleRatingChange(i, e) {
    const newRatings = ratings.slice();
    newRatings[i].rating = e.target.value;
    setRatings(newRatings);
  }

  function handleContentChange(i, e) {
    const newRatings = ratings.slice();
    newRatings[i].content = e.target.value;
    setRatings(newRatings);
  }

  function save() {
    fetch('/save_edits', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(ratings),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      });
  }

  let reviews = ratings.map(
    (review, i) => <Rating
      username={review.username}
      rating={review.rating}
      content={review.content}
      onDelete={() => handleDelete(i)}
      onEdit={(e) => handleContentChange(i, e)}
      onRate={(e) => handleRatingChange(i, e)}
    />);

    useEffect(() => {
      console.log("useEffect called");
      fetch('/get_reviews', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      })
        .then((response) => response.json())
        .then((data) => {
          setRatings(data);
        });
    }, []);
  
  return (
    <div className="App">
      <h1>Your reviews:</h1>
      {reviews}
      <button onClick={save}>Save changes!!</button>
    </div>
  );
}

export default App;
