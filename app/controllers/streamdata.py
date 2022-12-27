from functools import partial
import logging

from app.models.candle import create_candle_with_duration
from bitflyer.bitflyer import Ticker

import constants
import settings

logger = logging.getLogger(__name__)

#TODO
from bitflyer.bitflyer import APIClient
from bitflyer.bitflyer import BfRealtimeTicker
api = APIClient(settings.api_key, settings.api_account)
bf = BfRealtimeTicker(settings.product_code)

class StreamData(object):

    def stream_ingestion_data(self):
        bf.get(callback=self.trade)

    def trade(self, ticker: Ticker):
        logger.info(f'action=trade ticker={ticker.__dict__}')
        if False == (ticker.__dict__['product_code'] is None) :
            for duration in constants.DURATIONS:
                is_created = create_candle_with_duration(ticker.product_code, duration, ticker)
                print(is_created)
        logger.info(f'action=null of ticker')

# singleton
stream = StreamData()
