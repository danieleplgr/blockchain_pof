import React, { useState } from 'react';
import Joke from './Joke';


function App() {
  const [userQuery, setUserQueryF] = useState("");

  const updateUserQuery = (event) => {
    console.log("userQuery => "+ userQuery);
    setUserQueryF(event.target.value);
  }

  const searchQuery = () => {
    window.open(`https://google.com/search?q=${userQuery}`);
  }

  const handleKeyPress = (event) => {
    if(event.key === 'Enter'){
      searchQuery();
    }
  }

  return (
    <div className="App">
      <input value={userQuery} onChange={updateUserQuery} onKeyPress={handleKeyPress} />
      <button onClick={searchQuery} >Search</button>
      <hr/>
      <Joke/>
    </div>

  );
}

export default App;
