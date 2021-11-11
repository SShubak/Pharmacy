from sqlalchemy import create_engine, Integer, String, Column, Date, ForeignKey, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, Date, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

engine = create_engine('mysql+pymysql://root:OlehSyniuk@localhost:3306/pp')

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'
    id=Column(Integer, primary_key=True)
    name=Column(String(45))
    surname=Column(String(45))
    login=Column(String(45))
    password=Column(String(45))

class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    total_cost=Column(Integer)
    user_id=Column(Integer, ForeignKey('user.id'))
    medicine_id=Column(Integer, ForeignKey('medicine.id'))

    user = relationship("User")
    medicine = relationship("Medicine")

class Medicine(Base):
    __tablename__ = 'medicine'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    expiration_date = Column(Date)
    cost = Column(Integer)
    amount_avaliable = Column(Integer)
