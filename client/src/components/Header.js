import React from 'react';
import { useHistory } from 'react-router-dom';
import '../App.css';
import logo from '../logo2.jpeg';

function Header({ toggleTheme }) {
  const history = useHistory();

  const handleActionClick = () => {
    history.push('/login');
  };

  const handleLoginSignupClick = () => {
    history.push('/login');
  };

  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="Logo" className="logo-img" />
      </div>
      <div className="dropdown">
        <button className="dropbtn">Actions</button>
        <div className="dropdown-content">
          <a href="#" onClick={handleActionClick}>Alerts</a>
          <a href="#" onClick={handleActionClick}>Trades</a>
          <a href="#" onClick={handleActionClick}>Wallet</a>
          <a href="#" onClick={handleActionClick}>Watchlist</a>
        </div>
      </div>
      <div className="dropdown-preferences">
        Preferences
        <div className="dropdown-content-preferences">
          <button onClick={toggleTheme}>Switch theme</button>
          <button onClick={handleLoginSignupClick}>Login/Signup</button>
        </div>
      </div>
    </header>
  );
}

export default Header;
