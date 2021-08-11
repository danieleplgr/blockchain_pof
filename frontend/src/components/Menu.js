import React from 'react';
import {Link} from "react-router-dom";

function Menu(){

    return (
        <div>
            <Link to="/blockchain" >See blockchain</Link><br/>
            <Link to="/transact" >Create transaction</Link><br/>
            <Link to="/" >Homepage</Link><br/>
        </div>
    )
}

export default Menu;