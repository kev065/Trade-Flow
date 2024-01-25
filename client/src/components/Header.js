import React from 'react';
import '../App.css';
import logo from '../logo2.jpeg';

function Header({ toggleTheme, isLoggedIn, setIsLoggedIn }) { // adds isLoggedIn and setIsLoggedIn as props
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
          {isLoggedIn ? <button onClick={handleLogout}>Logout</button> : null} // to conditionally render the Logout button
        </div>
      </div>
    </header>
  );
}

export default Header;

