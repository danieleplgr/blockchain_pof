import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './components/App';
import {Router, Switch, Route} from 'react-router-dom';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';
import TransactionPool from './components/TransactionPool';
import history from "./history";


ReactDOM.render(
  <Router history={history} >
    <Switch>
      <Route path="/" exact={true} component={App} />
      <Route path="/blockchain" component={Blockchain} />
      <Route path="/transact" component={ConductTransaction} />
      <Route path="/transactions" component={TransactionPool} />
    </Switch>
  </Router>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
