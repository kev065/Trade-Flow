import React, { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import Chart from 'chart.js/auto';
import 'chartjs-plugin-zoom';

const LandingPage = () => {
  const [symbol, setSymbol] = useState('');
  const [priceData, setPriceData] = useState([]);
  const [socket, setSocket] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const newSocket = new W3CWebSocket('wss://stream.binance.com:9443/ws/btcusdt@trade');

    newSocket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      const { T: time, p: price } = data;
      setPriceData((prevData) => [...prevData, { time, price }]);
    };

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const subscribeToSymbol = () => {
    if (socket) {
      socket.close();
      setSocket(null);
    }

    const newSocket = new W3CWebSocket(`wss://stream.binance.com:9443/ws/${symbol.toLowerCase()}usdt@trade`);

    newSocket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      const { T: time, p: price } = data;
      setPriceData((prevData) => [...prevData, { time, price }]);
    };

    setSocket(newSocket);
  };

  useEffect(() => {
    if (chartRef.current && priceData.length > 0) {
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
              // y-axis configuration
              title: {
                display: true,
                text: 'Price',
              },
              suggestedMin: 40000, 
              suggestedMax: 40300,
            },
          },
          plugins: {
            zoom: {
              pan: {
                enabled: true,
                mode: 'x',
              },
              zoom: {
                wheel: {
                  enabled: true,
                },
                pinch: {
                  enabled: true,
                },
                mode: 'x',
              },
            },
          },
        },
      };

      const newChart = new Chart(ctx, chartConfig);

      chartRef.current.chart = newChart;
    }
  }, [priceData]);

  return (
    <div>
      <h1>Real-time Price Chart</h1>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Enter Symbol"
      />
      <button onClick={subscribeToSymbol}>Subscribe</button>
      <canvas ref={chartRef} width="400" height="200" />
    </div>
  );
};

export default LandingPage;
