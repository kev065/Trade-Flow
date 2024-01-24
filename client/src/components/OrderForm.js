import React, { useState } from 'react';
import axios from 'axios';

function OrderForm() {
  const [orderType, setOrderType] = useState('');
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
      <label>
        Order Type:
        <input type="text" value={orderType} onChange={e => setOrderType(e.target.value)} />
      </label>
      <label>
        Order Size:
        <input type="number" value={orderSize} onChange={e => setOrderSize(e.target.value)} />
      </label>
      <div>
        <button type="button" onClick={handleBuy}>Buy</button>
        <button type="button" onClick={handleSell}>Sell</button>
      </div>
    </form>
  );
}

export default OrderForm;
