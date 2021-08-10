import React, {useState, useEffect} from 'react';
import { API_BASE_URL } from "../config";
import Block from './Block';


function Blockchain(){
    const [blockchain, setBlockchain] = useState([]);

    useEffect(()=>{
        fetch(`${API_BASE_URL}/blockchain`)
            .then(response => response.json())
            .then(data => setBlockchain(data))
    }, []);


    return(
        <div className="Blockchain">
            <h3>Blockchain</h3>
            <div>{blockchain.map( block => {
                return <Block key={block.hash} block={block} />
            }  
            )}</div>
        </div>
    )
}

export default Blockchain;