import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import OrderForm from './components/OrderForm';
import Login from './components/Login'; 
import Register from './components/Register';
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

  const location = useLocation();

  return (
    <div className={`App ${theme}`}>
      {location.pathname !== '/login' && <Header toggleTheme={toggleTheme} isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />} 
      {location.pathname !== '/login' && <div className="chart"><LandingPage /></div>}
      {location.pathname !== '/login' && <div className="order-form"><OrderForm isLoggedIn={isLoggedIn} /></div>}
      <Routes>
        <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}

export default function AppWithRouter() {
  return (
    <Router>
      <App />
    </Router>
  );
}
