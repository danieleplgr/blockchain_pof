import React, {useState, useEffect } from 'react';

function Joke(){
    // setJoke cause a RENDER of the component!!
    const [joke, setJoke] = useState({});

    // init func on render (async - not blocking)   
    // RUN:every time a render of the component is called
    const observedVarsToReRunRender = []; // never re-render (prevent infinity loop)
    useEffect(()=>{
        fetch("https://official-joke-api.appspot.com/jokes/random")
            .then(response => response.json())
            .then(data => {
                console.log(`Data fetched `, data);
                setJoke(data);
            })
        console.log("Retrieving data.... ");
    }, observedVarsToReRunRender);

    const { setup, punchline } = joke;

    return (
        <div>
            <h3>Joke</h3>
            <p>{setup}</p>
            <p><em>{punchline}</em></p>
        </div>
    )
}

export default Joke;