import logging
import sys
from datetime import datetime
import app.models
from threading import Thread

from app.controllers.webserver import start

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

    # stream = StreamData()
    # for i in range(0, 1000):
    #     stream.stream_ingestion_data()
    #     time.sleep(0.5)
    # from app.models.dfcandle import DataFrameCandle
    # df = DataFrameCandle(settings.product_code, settings.trade_duration)
    # df.set_all_candles(settings.past_period)
    # print(df.value)
    # serverThread = Thread(target=start)
    # serverThread.start()

    # serverThread.join()


    # from app.models.dfcandle import DataFrameCandle
    # import talib
    # import numpy as np

    # df = DataFrameCandle(settings.product_code,
    #                      settings.trade_duration)
    # df.set_all_candles(100)
    # df.add_sma(7)
    # print(df.value)

    from app.models.events import SignalEvent
    import datetime
    import settings
    import constants

    now = datetime.datetime.utcnow()
    s = SignalEvent(time=now, product_code=settings.product_code, side=constants.BUY, price=100.0, units=1)
    s.save()

    signal_events = SignalEvent.get_signal_events_by_count(10)
    for signal_event in signal_events:
        print(signal_event.value)

    now = now - datetime.timedelta(minutes=10)
    signal_events = SignalEvent.get_signal_events_after_time(now)
    for signal_event in signal_events:
        print(signal_event.value)


    # streamThread = Thread(target=stream.stream_ingestion_data)
    # serverThread = Thread(target=start)

    # streamThread.start()
    # serverThread.start()

    # streamThread.join()
    # serverThread.join()
