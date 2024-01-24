import React, { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import Chart from 'chart.js/auto';

const LandingPage = () => {
  const [symbol, setSymbol] = useState('btcusdt');
  const [priceData, setPriceData] = useState([]);
  const [socket, setSocket] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    subscribeToSymbol();
    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, []);

  const subscribeToSymbol = () => {
    // this unsubscribes from the current symbol
    if (socket) {
      socket.close();
      setSocket(null);
    }

    // this subscribes to new symbol
    const newSocket = new W3CWebSocket(`wss://stream.binance.com:9443/ws/${symbol.toLowerCase()}@trade`);

    newSocket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      const { T: time, p: price } = data;

      const date = new Date(time);
      const readableTime = date.toLocaleTimeString();
      setPriceData((prevData) => [...prevData, { time: readableTime, price }]);
    };

    setSocket(newSocket);
  };

  useEffect(() => {
    if (chartRef.current && priceData.length > 0) {
      // destroys the existing chart if it exists - this helped solve an annoying error
      if (chartRef.current.chart) {
        chartRef.current.chart.destroy();
      }
  
      const ctx = chartRef.current.getContext('2d');
  
      const chartConfig = {
        type: 'line',
        data: {
          labels: priceData.map((data) => data.time),
          datasets: [
            {
              label: 'Price',
              data: priceData.map((data) => data.price),
              borderColor: 'blue',
              fill: false,
            },
          ],
        },
        options: {
          scales: {
            x: {
              type: 'category',
              labels: priceData.map((data) => data.time),
            },
            y: {
              // y-axis configuration - will add this
            },
          },
        },
      };
  
      // creates a new chart
      const newChart = new Chart(ctx, chartConfig);
  
      // attaches the chart instance to the canvas element
      chartRef.current.chart = newChart;
    }
  }, [priceData]);
  

  return (
    <div>
      <h1>Real-Time Price Chart</h1>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Enter Symbol"
      />
      <button onClick={subscribeToSymbol}>View</button>
      <canvas ref={chartRef} width="400" height="200" />
    </div>
  );
};

export default LandingPage;