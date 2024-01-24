import React, { useState, useEffect, useRef } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';

const LandingPage = () => {
  const [symbol, setSymbol] = useState('btcusdt');
  const [priceData, setPriceData] = useState([]);
  const [socket, setSocket] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const newSocket = new W3CWebSocket(`wss://stream.binance.com:9443/ws/${symbol}@trade`);

    newSocket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      const { T: time, p: price } = data;
      setPriceData((prevData) => [...prevData, { t: time, y: price }]);
    };

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [symbol]);

  useEffect(() => {
    if (!chartRef.current) {
      return;
    }

    if (chartRef.current.chart) {
      chartRef.current.chart.data.datasets[0].data = priceData;
      chartRef.current.chart.update();
    } else {
      const ctx = chartRef.current.getContext('2d');
      const newChart = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [
            {
              label: 'Price',
              data: priceData,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 1,
              fill: false,
            },
          ],
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'second',
              },
            },
            y: {
              // y-axis - will update values
            },
          },
        },
      });

      chartRef.current.chart = newChart;
    }
  }, [priceData]);

  const subscribeToSymbol = () => {
    if (socket) {
      socket.close();
      setSocket(null);
    }

    const newSocket = new W3CWebSocket(`wss://stream.binance.com:9443/ws/${symbol.toLowerCase()}@trade`);

    newSocket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      const { T: time, p: price } = data;
      setPriceData((prevData) => [...prevData, { t: time, y: price }]);
    };

    setSocket(newSocket);
  };

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
