from __future__ import annotations
import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = db.create_engine('sqlite:///sucden.db')

Session = sessionmaker(bind=engine)
session = Session()

# TODO: Haven't really touched base on this, very WiP

class TradeSchema(Base):
    __tablename__ = 'trades'

    tradeId = db.Column(db.String, primary_key=True)

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

Base.metadata.create_all(engine)
