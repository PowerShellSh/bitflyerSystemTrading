import logging
import sys
from datetime import datetime
import app.models


from bitflyer.bitflyer import APIClient
from bitflyer.bitflyer import Ticker
from app.models.candle import factory_candle_class
from app.models.candle import create_candle_with_duration
from bitflyer.bitflyer import BfRealtimeTicker
from threading import Thread
from app.controllers.streamdata import StreamData


import time
import settings


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


if __name__ == "__main__":

    # now1 = datetime.timestamp(datetime(2020, 1, 1, 1, 0, 0))
    # now2 = datetime.timestamp(datetime(2020, 1, 1, 1, 0, 1))
    # now3 = datetime.timestamp(datetime(2020, 1, 1, 1, 0, 2))
    # now4 = datetime.timestamp(datetime(2020, 1, 1, 1, 1, 0))

    # ticker = Ticker(settings.product_code, now1, 100, 100, 1)
    # create_candle_with_duration(settings.product_code, '1m', ticker)
    # ticker = Ticker(settings.product_code, now2, 110, 110, 1)
    # create_candle_with_duration(settings.product_code, '1m', ticker)

    # ticker = Ticker(settings.product_code, now2, 80, 80, 1)
    # create_candle_with_duration(settings.product_code, '1m', ticker)

    # ticker = Ticker(settings.product_code, now4, 200, 200, 1)
    # create_candle_with_duration(settings.product_code, '1m', ticker)

    # streamThread = Thread(target=stream.stream_ingestion_data)
    # streamThread.start()

    stream = StreamData()
    for i in range(0, 100):
        stream.stream_ingestion_data()
        time.sleep(0.5)
