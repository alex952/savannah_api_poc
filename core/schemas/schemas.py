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

#########################
#### PRODUCT SCHEMAS ####
#########################

product_association_table = db.Table('association', Base.metadata,
    db.Column('underlying_name', db.ForeignKey('underlyings.name'), primary_key=True),
    db.Column('maturity_name', db.ForeignKey('maturities.name'), primary_key=True)
)

class UnderlyingSchema(Base):
    __tablename__ = 'underlyings'

    name = db.Column(db.String, primary_key=True)
    maturities = relationship(
        "MaturitySchema",
        secondary=product_association_table,
        back_populates="products")

    @classmethod
    def get_all(cls):
        with Session() as session:
            return session.query(cls).all()


class MaturitySchema(Base):
    __tablename__ = 'maturities'

    name = db.Column(db.String, primary_key=True)
    products = relationship(
        "UnderlyingSchema",
        secondary=product_association_table,
        back_populates="maturities")

    @classmethod
    def get_all(cls):
        with Session() as session:
            return session.query(cls).all()



# class ProductSchema(Base):
#     __tablename__ = 'maturities'
#     underlying_name = 
#     maturity_name = 


#######################
#### QUOTE SCHEMAS ####
#######################

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


#######################
#### TRADE SCHEMAS ####
#######################


class TradeSchema(Base):
    __tablename__ = 'trades'

    tradeId = db.Column(db.String, primary_key=True)

    @classmethod
    def get_all(cls):
        with Session() as session:
            return session.query(cls).all()


#####################
#### VOL SCHEMAS ####
#####################


## WIP ##
class VolCurveType(Enum):
    Strike = "Strike"
    Delta  = "Delta"

class VolCurve(Base):
    __tablename__ = 'vol_curve'

    underlying = db.Column(db.String, primary_key=True)
    maturity = db.Column(db.Date, primary_key=True)
    vol_curve_date   = db.Column(db.Date, primary_key=True)
    vol_curve_source = db.Column(db.String, primary_key=True, server_default="LME")
    vol_type         = db.Column(db.Enum(VolCurveType), primary_key=True)
    # vol_curve_point  = db.Column(db.Integer, primary_key=True)

    value            = db.Column(db.Float)

    @classmethod
    def get(cls, underlying, maturity, vol_type, t, source="LME" ):
        with Session() as session:
            return session.query(cls)\
                .filter(VolCurve.underlying == underlying)\
                .filter(VolCurve.maturity == maturity)\
                .filter(VolCurve.vol_type == vol_type)\
                .filter(VolCurve.vol_curve_source == source)\
                .filter(VolCurve.vol_curve_date == t)\
                .with_entities(VolCurve.value).all()


Base.metadata.create_all(engine)
