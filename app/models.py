from sqlalchemy import Column, Integer, SmallInteger, Date, DateTime, func
from app.db import Base


class LottoDraw(Base):
    __tablename__ = "lotto_draws"

    id = Column(Integer, primary_key=True, autoincrement=True)
    draw_no = Column(Integer, nullable=False, unique=True)
    draw_date = Column(Date, nullable=False)

    n1 = Column(SmallInteger, nullable=False)
    n2 = Column(SmallInteger, nullable=False)
    n3 = Column(SmallInteger, nullable=False)
    n4 = Column(SmallInteger, nullable=False)
    n5 = Column(SmallInteger, nullable=False)
    n6 = Column(SmallInteger, nullable=False)

    bonus = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())