import React, {useState, useEffect} from 'react';
import { API_BASE_URL } from "../config";
import Block from './Block';
import {Button} from "react-bootstrap";



const PAGE_RANGE = 3;

function Blockchain(){
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLenght, setBlockchainLenght] = useState(0);

    // param is an object that contains the 2 keys: destruct
    const fetchBlockchainPage = ({start, end}) => {
        fetch(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
            .then(response => response.json())
            .then(data => setBlockchain(data))
    }


    useEffect(()=>{
        fetchBlockchainPage({start: 0, end: PAGE_RANGE});
        
        fetch(`${API_BASE_URL}/blockchain/lenght`)
            .then(response => response.json())
            .then(data => setBlockchainLenght(data))
    }, []);

    const pageNumbers = [];
    for (let i=0; i<Math.ceil(blockchainLenght/PAGE_RANGE); i++){
        pageNumbers.push(i);
    }

    return(
        <div className="Blockchain">
            <h3>Blockchain</h3>
            <div>{blockchain.map( block => {
                return <Block key={block.hash} block={block} />
            }  
            )}</div>

            <div>
                {
                    pageNumbers.map(page => {
                        const start = page * PAGE_RANGE;
                        const end = (page+1) * PAGE_RANGE;

                        return (
                            <span key={page}>
                                <Button size="sm" variant="info" onClick={ () => fetchBlockchainPage({start, end})} >{page+1}</Button>
                            </span>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Blockchain;