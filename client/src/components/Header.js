import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import logo from '../logo2.jpeg';

function Header({ toggleTheme, isLoggedIn, setIsLoggedIn }) { 
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

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
      <div className="dropdown-preferences">
        Preferences
        <div className="dropdown-content-preferences">
          <button onClick={toggleTheme}>Toggle theme</button>
          {isLoggedIn ? <button onClick={handleLogout}>Logout</button> : <><button onClick={() => navigate('/login')}>Login</button><button onClick={() => navigate('/register')}>Register</button></>} 
        </div>
      </div>
    </header>
  );
}

export default Header;


