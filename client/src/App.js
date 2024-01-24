import React, { useState } from 'react';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import OrderForm from './components/OrderForm';
import './light.css';
import './dark.css';

function App() {
  const [theme, setTheme] = useState('light'); // default theme is light

  const toggleTheme = () => {
    if (theme === 'light') {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  };

  return (
    <div className={`App ${theme}`}>
      <Header toggleTheme={toggleTheme} />
      <div className="chart">
        <LandingPage />
      </div>
      <div className="order-form">
        <OrderForm />
      </div>
    </div>
  );
}

export default App;


