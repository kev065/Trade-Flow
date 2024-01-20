import requests

class BinanceService:
    BASE_URL = 'https://api.binance.com'  

    def get_price(self, symbol):
        """Get the latest price for a symbol."""
        response = requests.get(f'{self.BASE_URL}/api/v3/ticker/price', params={'symbol': symbol})
        response.raise_for_status()  # Raises an exception if the request failed
        data = response.json()
        return float(data['price'])
