import logging
import sys
import datetime

from bitflyer.bitflyer import APIClient
from app.models.base import BtcJpyBaseCandle1M
import settings
import app.models


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


if __name__ == "__main__":
    api_client = APIClient(settings.api_key, settings.api_account)
    # balance = api_client.get_balance()
    # print(balance.available)
    # print(balance.currency)
    # ticker = api_client.get_ticker(settings.product_code)
    # print(ticker.product_code)
    # print(ticker.ask)
    # print(ticker.bid)
    # print(ticker.volume)
    # print(ticker.truncate_date_time('5s'))
    # print(ticker.truncate_date_time(settings.trade_duration))
    # print(ticker.truncate_date_time('1h'))
    # print(ticker.time)
    # print('mid : ', ticker.mid_price)
    api_client.get_realtime_ticker(settings.product_code)



    # now1 = datetime.datetime(2022,1,2,3,4,5)
    # BtcJpyBaseCandle1M.create(now1, 1.0, 2.0, 3.0, 4.0, 5)
    
