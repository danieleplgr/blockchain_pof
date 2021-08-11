import React, {useState, useEffect} from 'react';
import { API_BASE_URL } from "../config";
import Menu from "./Menu";
import Transaction from './Transaction';
import {Button} from "react-bootstrap";
import history from "../history";


const TRANSACTIONS_REFRESH_INTERVAL = 5000;

function TransactionPool(){
    const [transactions, setTransactions] = useState([]);    

    const fetchTransactionsInPool = () => {
        fetch(`${API_BASE_URL}/transactions`)
            .then(response => response.json())
            .then((data) => {
                console.log("received transactions in pool", data)
                setTransactions(data)
            });
    }

    const fetchMineBlock = () => {
        fetch(`${API_BASE_URL}/blockchain/mine`)
            .then(() => {
                alert("Success");
                history.push("/blockchain");
            });
    }

    useEffect(()=>{
        fetchTransactionsInPool(); 
        const invervalId = setInterval(fetchTransactionsInPool, TRANSACTIONS_REFRESH_INTERVAL);

        // a return here is a hook into the unmount-component..
        return () => { clearInterval(invervalId); }
        
    }, []);

    return (
        <div className="TransactionPool">
            <Menu/>
            <h4>Transaction pool</h4>

            {transactions.map(transaction => (
                <div key={transaction.id}>
                    <hr/>
                    <Transaction transaction={transaction} />
                </div>
            ))}
            
            <hr/>
            <Button variant="danger" onClick={fetchMineBlock}>Mine a block</Button>
        </div>
    )
}

export default TransactionPool;