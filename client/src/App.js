import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import OrderForm from './components/OrderForm';
import Login from './components/Login';
import './light.css';
import './dark.css';

function App() {
  const [theme, setTheme] = useState('light'); 
  const [isLoggedIn, setIsLoggedIn] = useState(false); 

  const toggleTheme = () => {
    if (theme === 'light') {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  };

  return (
    <Router>
      <div className={`App ${theme}`}>
        <Header toggleTheme={toggleTheme} isLoggedIn={isLoggedIn} />
        <div className="chart">
          <LandingPage />
        </div>
        <div className="order-form">
          {isLoggedIn ? <OrderForm /> : <Redirect to="/login" />}
        </div>
        <Route path="/login">
          <Login setIsLoggedIn={setIsLoggedIn} />
        </Route>
      </div>
    </Router>
  );
}

export default App;



