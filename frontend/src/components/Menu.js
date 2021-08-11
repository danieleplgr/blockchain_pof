import React from 'react';
import {Link} from "react-router-dom";

function Menu(){

    return (
        <div>
            <Link to="/" >Homepage</Link><br/>
            <Link to="/blockchain" >See blockchain</Link><br/>
            <Link to="/transact" >Create transaction</Link><br/>
            <Link to="/transactions">Transactions pool</Link> 
        </div>
    )
}

export default Menu;