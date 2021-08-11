import React, {useState, useEffect} from 'react';
import {FormGroup, Button, FormControl} from 'react-bootstrap';
import { API_BASE_URL } from '../config';
import history from "../history";


function ConductTransaction(){
    const [amount, setAmount] = useState(0);
    const [recipient_address, setRecipient] = useState("");
    const [knownAddresses, setKnowAddresses] = useState([]);

    useEffect(() => {
        fetch(`${API_BASE_URL}/wallet/know-addresses`)
            .then(response => response.json())
            .then(data => setKnowAddresses(data));
    }, []);

    const submitTransaction = () => {
        fetch(`${API_BASE_URL}/wallet/transact`, { 
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({recipient_address, amount})
        }).then(response => response.json())
          .then(data => {
              console.log("Transaction submitted");
              alert("Success");
              history.push("/transactions");
          });
    }

    const updateRecipient = (event) => {
        setRecipient(event.target.value);
    }
    const updateAmount = (event) => {
        setAmount(Number(event.target.value));
    }

    return (
        <div className="ConductTransaction">
            <h3>Conduct transaction</h3>
            <br/>
            <FormGroup>
                <FormControl input="text" placeholder="recipient_address" value={recipient_address} onChange={updateRecipient} /> 
            </FormGroup>

            <FormGroup>
                <FormControl input="number" placeholder="amount" value={amount} onChange={updateAmount} /> 
            </FormGroup>

            <div>
                <Button variant="danger" onClick={submitTransaction}> 
                    Submit
                </Button>
            </div>
            <br/>

            <div>
                <h4>Known addresses</h4>
                {knownAddresses.map( (knowAddress, i) => (
                    <span key={knowAddress} >
                        <u>{knowAddress}</u>{i !== knownAddresses.length-1 ? ', ': ''}
                    </span>
                ) )}
            </div>
        </div>
    )
}

export default ConductTransaction;