import React from 'react';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import OrderForm from './components/OrderForm';
import './App.css';


function App() {
  return (
    <div className="App">
      <Header />
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

