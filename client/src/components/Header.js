import React from 'react';
import '../App.css';
import logo from '../logo2.jpeg';

function Header() {
  return (
    <header className="header">
      <div className="logo">
      <img src={logo} alt="Logo" className="logo-img" />
      </div>
      <div className="dropdown">
        <button className="dropbtn">Actions</button>
        <div className="dropdown-content">
          <a href="#">Alerts</a>
          <a href="#">Trades</a>
          <a href="#">Wallet</a>
          <a href="#">Watchlist</a>
        </div>
      </div>
      <div className="preferences">Preferences</div>
    </header>
  );
}

export default Header;