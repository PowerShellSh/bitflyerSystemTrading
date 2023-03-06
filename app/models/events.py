import datetime

import omitempty
from sqlalchemy import Column
from sqlalchemy import desc
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from app.models.base import session_scope
from app.models.base import Base
import constants
import settings


class SignalEvent(Base):
    __tablename__ = 'signal_event'

    time = Column(DateTime, primary_key=True,nullable=False)
    poduct_code = Column(String)
    side = Column(String)
    price = Column(Float)
    units = Column(Integer)

    def save(self):
        with session_scope() as session:
            session.add(self)

    @property
    def value(self):
        dict_values = omitempty({
            'time': self.time,
            'product_code': self.product_code,
            'price': self.price,
            'units': self.units,
        })
        if not dict_values:
            return None
        else:
            return dict_values

    @classmethod
    def get_signal_events_by_count(cls, count,product_code=settings.product_code):
        with session_scope() as session:
            rows = session.query(cls).filter(cls.product_code == product_code).order_by(desc(cls.time)).limit(count).all()
            if rows is None:
                return []
            rows.reverse()
            return rows

    @classmethod
    def get_signal_events_after_time(cls, time):
        with session_scope() as session:
            rows = session.query(cls).filter(cls.time >= time).all()

            if rows is None:
                return []

            return rows
