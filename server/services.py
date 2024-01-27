import os
import hmac
import time
import hashlib
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

class BinanceService:
    BASE_URL = 'https://testnet.binancefuture.com'
    API_KEY = os.getenv("BINANCE_API_KEY")
    SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")


    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def get_price(self, symbol):
        headers = {
            'X-MBX-APIKEY': self.API_KEY
        }
        try:
            response = requests.get(f'{self.BASE_URL}/fapi/v1/ticker/price', headers=headers, params={'symbol': symbol})
            response.raise_for_status() 
            data = response.json()
            return float(data['price'])
        except requests.exceptions.RequestException as err:
            self.logger.error(f"Failed to get price for {symbol}. Error: {err}")
            return None

    def place_order(self, symbol, side, quantity):
        timestamp = int(time.time() * 1000)
        query_string = f'symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}'
        signature = hmac.new(bytes(self.SECRET_KEY, 'utf-8'), msg=bytes(query_string, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

        headers = {
            'X-MBX-APIKEY': self.API_KEY
        }
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity,
            'timestamp': timestamp,
            'signature': signature
        }
        try:
            response = requests.post(f'{self.BASE_URL}/fapi/v1/order', headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            self.logger.error(f"Failed to place order on Binance. Error: {err}")
            return None

    

    

