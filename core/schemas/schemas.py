from __future__ import annotations
import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = db.create_engine('sqlite:///sucden.db')

Session = sessionmaker(bind=engine)
session = Session()

class ProjectSchema(Base):
    __tablename__ = 'projects'

    name = db.Column(db.String, primary_key=True)

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

# class Task(BaseModel):
#     title: str
#     priority: Optional[PrioEnum] = None
#     project: Optional[Project] = None
#     tags: List[str] = []
#     due_date: Optional[datetime] = None
#     wait_date: Optional[datetime] = None
#     depends: List[Task] = []
# 
#     class Config:
#         orm_mode = True
# 
# Task.update_forward_refs()

Base.metadata.create_all(engine)
