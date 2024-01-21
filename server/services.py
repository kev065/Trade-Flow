import os
import requests
from dotenv import load_dotenv

load_dotenv() 

class BinanceService:
    BASE_URL = 'https://api.binance.com'  
    API_KEY = os.getenv("BINANCE_API_KEY")
    SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

    def get_price(self, symbol):
        """Get the latest price for a symbol."""
        headers = {
            'X-MBX-APIKEY': self.API_KEY
        }
        response = requests.get(f'{self.BASE_URL}/api/v3/ticker/price', headers=headers, params={'symbol': symbol})
        response.raise_for_status()  # Raises an exception if the request failed
        data = response.json()
        return float(data['price'])
