import logging
import sys
import hashlib
import hmac
import requests
import time
from datetime import datetime
import dateutil.parser
import math
import constants
import websocket
import json

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class Ticker(object):
    def __init__(self, product_code, timestamp, bid, ask, volume):
        self.product_code = product_code
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.volume = volume

    @property
    def mid_price(self):
        return (self.bid + self.ask) / 2

    @property
    def time(self):
        return datetime.utcfromtimestamp(self.timestamp)

    def truncate_date_time(self, duration):
        ticker_time = self.time
        if duration == constants.DURATION_5S:
            new_sec = math.floor(self.time.second / 5) * 5
            ticker_time = datetime(
                self.time.year, self.time.month, self.time.day,
                self.time.hour, self.time.minute, new_sec)
            time_format = '%Y-%m-%d %H:%M:%S'
        elif duration == constants.DURATION_1M:
            time_format = '%Y-%m-%d %H:%M'
        elif duration == constants.DURATION_1H:
            time_format = '%Y-%m-%d %H'
        else:
            logger.warning('action=truncate_date_time error=no_datetime_format')
            return None

        str_date = datetime.strftime(ticker_time, time_format)
        return datetime.strptime(str_date, time_format)


class Balance(object):
    def __init__(self, currency, available):
        self.currency = currency
        self.available = available


class APIClient(object):
    def __init__(self, api_key, api_account):
        self.api_key = api_key
        self.api_account = api_account

    def header(self, method: str, endpoint: str, body: str) -> dict:
        timestamp = str(time.time())
        if body == '':
            message = timestamp + method + endpoint
        else:
            message = timestamp + method + endpoint + body
        signature = hmac.new(self.api_account.encode('utf-8'), message.encode('utf-8'),
                            digestmod=hashlib.sha256).hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'ACCESS-KEY': self.api_key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': signature
        }
        return headers

    def get_balance(self) -> Balance:
        base_url = 'https://api.bitflyer.com'
        endpoint = '/v1/me/getbalance'

        headers = self.header('GET', endpoint=endpoint, body='')
        try:
            response = requests.get(base_url + endpoint, headers=headers)
        except Exception as e:
            logger.error(f'action-get_balance error={e}')
        else:
            result = response.json()
            btc = [x for x in result if x['currency_code'] == 'BTC']
            available = float(btc[0]['available'])
            currency = btc[0]['currency_code']
            return Balance(currency, available)


    def get_ticker(self, product_code) -> Ticker:
        base_url = 'https://api.bitflyer.com'
        endpoint = '/v1/ticker'
        params = {
            'product_code': product_code
        }
        try:
            response = requests.get(base_url + endpoint, params={"product_code": product_code})
            result = response.json()
        except Exception as e:
            logger.error(f'action=get_ticker error={e}')
            raise
        product_code = result['product_code']
        timestamp = datetime.timestamp(
            dateutil.parser.parse(result['timestamp']))
        bid = float(result['best_bid'])
        ask = float(result['best_ask'])
        volume = float(result['volume'])
        return Ticker(product_code, timestamp, bid, ask, volume)
    

    def get_realtime_ticker(self, product_code):
        product_code = product_code

        web_socket_url = 'wss://ws.lightstream.bitflyer.com/json-rpc'
        channel = f'lightning_ticker_{product_code}'
        ws = websocket.WebSocketApp(web_socket_url,
                                    on_message=self.get_real_ticker_on_message,
                                    on_open=lambda wss: wss.send(json.dumps({'method': 'subscribe',
                                                                            'params': {'channel': channel}}))
                                    )
        try:
            ws.run_forever()
        except Exception as e:
            # ロギング処理するとか
            raise
    

    def get_real_ticker_on_message(self, ws, message):
        # WebsocketでJSON-RPCから情報が来た時の処理
        message = json.loads(message)['params']
        result = message.get('message')
        product_code = result['product_code']
        timestamp = datetime.timestamp(
            dateutil.parser.parse(result['timestamp']))
        bid = float(result['best_bid'])
        ask = float(result['best_ask'])
        volume = float(result['volume'])
        print(message)
        return Ticker(product_code, timestamp, bid, ask, volume)
        