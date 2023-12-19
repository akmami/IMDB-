import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLink } from '@fortawesome/free-solid-svg-icons';
import React, { useState, useEffect } from 'react';
import './App.css';

const backendURL = 'http://127.0.0.1:5000/';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [movieData, setMovieData] = useState(null);
  const [loadingTime, setLoadingTime] = useState(null);

  useEffect(() => {
    console.log('movieData has been updated:');
  }, [movieData]); 

  const handleSearch = async () => {

    if (!searchQuery.trim()) {
      setMovieData(null);
      return;
    }

    console.log("Search query: " + searchQuery);
    
    try {
      try {
        const startTime = new Date();

        const response = await fetch(backendURL, {
          method: 'POST',
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({'query': searchQuery}),
        });

        if (!response.ok) {
          console.log(response);
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log("data.movies: " + data.movies);

        const endTime = new Date();
        const timeTaken = (endTime - startTime) / 1000;

        setMovieData(data.movies);
        setLoadingTime(timeTaken);
      } catch (error) {
        console.error('Error sending HTTP request:', error);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>IMDb Search</h1>
      <div style={styles.searchContainer}>
        <input
          type="text"
          value={searchQuery}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSearch();
            }
          }}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Enter movie title"
          style={styles.searchInput}
        />
        <button onClick={handleSearch} style={styles.searchButton}>
          Search
        </button>
      </div>

      {loadingTime && (
        <p style={styles.loadingTime}>
          Query took {loadingTime.toFixed(5)} seconds
        </p>
      )}

      {movieData && movieData.length > 0 && (
        <div style={styles.movieContainer}> 
          { movieData.map((movie, index) => (
              <div key={movie.imdb_title_id} style={styles.movieCard}>
                <div style={styles.movieHeaderContainer}>
                  <p style={styles.movieNumber}>{index + 1}</p>
                  <h2 style={styles.movieTitle}>{movie.title}</h2>
                  <a
                    style={{ marginLeft: '8px' }}
                    href={`https://www.imdb.com/title/${movie.imdb_title_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <FontAwesomeIcon icon={faLink} style={styles.navigationIcon} />
                  </a>
                </div>
                <p>Plot: {movie.description}</p>
                <p>Year: {movie.year}</p>
                <p>Genre: {movie.genre}</p>
                <p>Duration: {movie.duration}</p>
                <p>Country: {movie.country}</p>
                <p>Language: {movie.language}</p>
                <p>Director: {movie.director}</p>
                <p>Writer: {movie.writer}</p>
                <p>Actors: {movie.actors}</p>
                <p>Average Votes: <span style={styles.averageVotes}>{movie.avg_vote}</span></p>
                <hr />
              </div>
            ))
          }
        </div>
        )
      }
    </div>
  );

}

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#1f1f1f',
    color: '#fff',
    padding: '20px',
  },
  header: {
    color: '#3498db',
  },
  searchContainer: {
    display: 'flex',
    marginBottom: '20px',
  },
  searchInput: {
    flex: 1,
    padding: '10px',
    fontSize: '16px',
    border: '1px solid #3498db',
    borderRadius: '5px 0 0 5px',
  },
  searchButton: {
    padding: '10px',
    fontSize: '16px',
    backgroundColor: '#3498db',
    color: '#fff',
    border: '1px solid #3498db',
    borderRadius: '0 5px 5px 0',
    cursor: 'pointer',
  },
  movieContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px',
    padding: '10px',
    margin: '5px',
    justifyContent: 'center',
  },
  movieCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.5)',
    border: '1px solid #ddd',
    borderRadius: '5px',
    padding: '15px',
    width: '330px',
  },
  movieHeaderContainer: {
    display: 'flex',
    alignItems: 'center',
  },
  loadingTime: {
    fontSize: '14px',
    opacity: '0.8',
    paddingLeft: '10px',
  },
  movieNumber: {
    color: 'yellow',
    fontSize: '23px',
    fontWeight: 'bold',
    marginTop: '4px',
    marginRight: '10px',
  },
  movieTitle: {
    color: '#fff',
  },
  navigationIcon: {
    width: '24px',
    height: '24px',
    cursor: 'pointer',
  },
  averageVotes: {
    color: 'yellow',
  },
  hr: {
    border: '0',
    height: '1px',
    backgroundColor: '#ddd',
    margin: '10px 0',
  },
};

export default App;