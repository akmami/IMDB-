import React, { useState } from 'react';
import './App.css';

const backendURL = 'http://127.0.0.1:5000/';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [movieData, setMovieData] = useState(null);

  const handleSearch = async () => {
    console.log("Search query: " + searchQuery);
    
    try {
      const url = backendURL;
      const movieTitle = 'The movie that related to dream within a dream';

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({'query': movieTitle}),
        });

        if (!response.ok) {
          console.log(response);
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("data.tfidf: " + data.tfidf) // TODO:
        console.log("data.bm25: " + data.bm25) // TODO:
      } catch (error) {
        console.error('Error sending HTTP request:', error);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <h1>IMDb Search</h1>
      <div>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Enter movie title"
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {movieData && (
        <div>
          <h2>{movieData.title}</h2>
          <p>Year: {movieData.year}</p>
          <p>Genre: {movieData.genre}</p>
          <p>Duration: {movieData.duration}</p>
          <p>Country: {movieData.country}</p>
          <p>Language: {movieData.language}</p>
          <p>Director: {movieData.director}</p>
          <p>Writer: {movieData.writer}</p>
          <p>Actors: {movieData.actors}</p>
          <p>Average Votes: {movieData.averageVotes}</p>
        </div>
      )}
    </div>
  );
}

export default App;