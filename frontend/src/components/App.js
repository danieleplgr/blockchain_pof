import React, {useState, useEffect} from 'react';
import logo from "../assets/logo.png";
import { API_BASE_URL } from "../config"; 
import Menu from "./Menu";


function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(()=>{
    fetch(`${API_BASE_URL}/wallet/info`)
      .then((response)=> response.json() )
      .then((data) => setWalletInfo(data) );
  }, []);

  const {address, balance} = walletInfo;

  return (
    <div className="App">
      <img className="logo" src={logo} alt="application-logo" />
      <h3>Welcome to pychain</h3>
      <br/>
        <Menu/>
      <br/>

      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
      <br/> 
    </div>

  );
}

export default App;
