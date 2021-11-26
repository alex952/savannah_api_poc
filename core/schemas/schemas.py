from __future__ import annotations
from enum import Enum
import sqlalchemy as db
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload

Base = declarative_base()

engine = db.create_engine('sqlite:///sucden.db')

Session = sessionmaker(bind=engine)
# session = Session()

# TODO: Haven't really touched base on this, very WiP

class QuoteLineSchema(Base):
    __tablename__ = 'quote_line'

    #Inputs side
    quote_line_id = db.Column(db.Integer, primary_key=True)

    side          = db.Column(db.String)
    basis         = db.Column(db.Float)
    strike_price  = db.Column(db.Float)
    vol           = db.Column(db.Float)
    interest      = db.Column(db.Float)
    dividend      = db.Column(db.Float)
    maturity      = db.Column(db.Date)

    quote         = db.Column(db.Integer, db.ForeignKey('quote.quote_id'))

class QuoteSchema(Base):
    __tablename__ = 'quote'

    quote_id      = db.Column(db.Integer, primary_key=True)
    quote_lines   = relationship("QuoteLineSchema")

    underlying    = db.Column(db.String)
    maturity      = db.Column(db.Date)
    strategy      = db.Column(db.String)
    counterparty  = db.Column(db.String)
    created_by    = db.Column(db.String)
    created_at    = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def get_all(cls):
        with Session() as session:
            return session.query(cls).options(joinedload(cls.quote_lines)).all()

    @classmethod
    def filter(cls, filter_field, filter_value):
        with Session() as session:
            if not filter_field:
                return session.query(cls).options(joinedload(cls.quote_lines)).all()
            else:
                return session.query(cls).filter(getattr(cls, filter_field) == filter_value).options(joinedload(cls.quote_lines)).all()

    @classmethod
    def store(cls, quote):
        with Session() as session:
            lines = []

            for q in quote.quote_lines:
                ql = QuoteLineSchema(**q.dict())
                session.add(ql)
                lines.append(ql)

            obj = cls(maturity=quote.maturity,
                      underlying=quote.underlying,
                      strategy=quote.strategy,
                      counterparty=quote.counterparty,
                      created_by=quote.created_by,
                      quote_lines=lines)
            session.add(obj)

            # I think it autocommits
            session.commit()


class TradeSchema(Base):
    __tablename__ = 'trades'

    tradeId = db.Column(db.String, primary_key=True)

    @classmethod
    def get_all(cls):
        with Session() as session:
            return session.query(cls).all()

Base.metadata.create_all(engine)
