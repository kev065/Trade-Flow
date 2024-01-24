import React, { useState } from 'react';
import axios from 'axios';

function OrderForm() {
  const [orderType, setOrderType] = useState('Market');
  const [orderSize, setOrderSize] = useState('');

  const handleBuy = event => {
    event.preventDefault();
    placeOrder('buy');
  };

  const handleSell = event => {
    event.preventDefault();
    placeOrder('sell');
  };

  const placeOrder = (type) => {
    axios.post('http://localhost:5555/order', {
      user_id: 1,  
      token_id: 'BTCUSDT',  
      order_type: type,
      quantity: orderSize,
      futures: false,  
    })
    .then(response => console.log('Order placed', response))
    .catch(error => console.error('Error placing order', error));
  };

  return (
    <form id="order-form">
      <div className="order-field">
        <label>Order Type:</label>
        <select value={orderType} onChange={e => setOrderType(e.target.value)}>
          <option value="Market">Market</option>
          <option value="Limit">Limit</option>
          <option value="Stop Limit">Stop limit</option>
          <option value="Stop Market">Stop Market</option>
          <option value="Trailing Stop">Trailing Stop</option>
          <option value="Post Only">Post Only</option>
          <option value="Scaled Order">Scaled Order</option>
        </select>
      </div>
      <div className="order-field">
        <label>Order Size:</label>
        <input type="number" value={orderSize} onChange={e => setOrderSize(e.target.value)} />
      </div>
      <div className="order-buttons">
        <button type="button" onClick={handleBuy}>Buy</button>
        <button type="button" onClick={handleSell}>Sell</button>
      </div>
    </form>
  );
}

export default OrderForm;

