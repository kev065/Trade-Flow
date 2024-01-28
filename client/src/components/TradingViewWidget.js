import React, { useEffect, useRef, memo } from 'react';

function TradingViewWidget() {
  const container = useRef();

  useEffect(() => {
    if (!document.getElementById('tradingview-widget-script')) {
      const script = document.createElement('script');
      script.id = 'tradingview-widget-script';
      script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';
      script.type = 'text/javascript';
      script.async = true;
      script.innerHTML = `{
        "autosize": true,
        "symbol": "BINANCE:BTCUSDT.P",
        "interval": "1",
        "timezone": "Africa/Nairobi",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "enable_publishing": true,
        "allow_symbol_change": true,
        "watchlist": [
          "BINANCE:BTCUSDT.P",
          "BINANCE:ETHUSDT.P",
          "BINANCE:SOLUSDT",
          "BINANCE:XRPUSDT.P",
          "BINANCE:DOGEUSDT.P",
          "BINANCE:DOTUSDT.P",
          "BINANCE:BNBUSDT.P",
          "BINANCE:TRXUSDT.P",
          "BINANCE:1000SHIBUSDT.P",
          "BINANCE:AVAXUSDT.P",
          "BINANCE:ADAUSDT.P",
          "BINANCE:LINKUSDT.P",
          "BINANCE:MATICUSDT.P",
          "BINANCE:ICPUSDT.P",
          "BINANCE:APTUSDT.P",
          "BINANCE:XMRUSDT.P",
          "BINANCE:ARBUSDT.P",
          "BINANCE:MKRUSDT.P",
          "BINANCE:AAVEUSDT.P",
          "BINANCE:LDOUSDT.P"
        ],
          "details": true,
          "hotlist": true,
          "calendar": true,
          "support_host": "https://www.tradingview.com"
        }`;
      container.current.appendChild(script);
    }
  }, []);

  return (
    <div className="tradingview-widget-container" ref={container} style={{ height: "100%", width: "100%" }}>
      <div className="tradingview-widget-container__widget" style={{ height: "calc(100% - 32px)", width: "100%" }}></div>
      <div className="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span className="blue-text">Track all markets on TradingView</span></a></div>
    </div>
  );
}


export default memo(TradingViewWidget);
