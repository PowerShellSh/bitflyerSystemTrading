from contextlib import contextmanager
import logging
import threading

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import settings

logger = logging.getLogger(__name__)
Base = declarative_base()
engine = create_engine(f'sqlite:///{settings.db_name}?check_same_thread=False')
Session = scoped_session(sessionmaker(bind=engine))
lock = threading.Lock()


@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        lock.acquire()
        yield session
        session.commit()
    except Exception as e:
        logger.error(f'action=session_scope, error={e}')
        session.rollback()
        raise
    finally:
        session.expire_on_commit = False
        lock.release()


def 



class BaseCandleMixin(object):
    time = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)

    @classmethod
    def create(cls, time, open, close, high, low, volume):
        candle = cls(
            time=time,
            open=open,
            close=close,
            high=high,
            low=low,
            volume=volume
        )
        try:
            with session_scope() as session:
                session.add(candle)
            return candle
        except IndentationError:
            return False

class BtcJpyBaseCandle1H(BaseCandleMixin, Base):
    __tablename__ = 'BTC_JPY_1H'


class BtcJpyBaseCandle1M(BaseCandleMixin, Base):
    __tablename__ = 'BTC_JPY_1M'


class BtcJpyBaseCandle5S(BaseCandleMixin ,Base):
    __tablename__ = 'BTC_JPY_5S'


def init_db():
    Base.metadata.create_all(bind=engine)