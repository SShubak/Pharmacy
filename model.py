from sqlalchemy import create_engine, Integer, String, Column, Date, ForeignKey, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

engine = create_engine('mysql+pymysql://root:root@localhost:3306/pharmacy')

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True)
    firstName = Column(String(45))
    lastName = Column(String(45))
    login = Column(String(45))
    password = Column(String(200))


class Order(Base):
    __tablename__ = 'order'
    id_order = Column(Integer, primary_key=True)
    id_medicine = Column(Integer, ForeignKey('medicine.id_medicine'))
    id_user = Column(Integer, ForeignKey('user.id_user'))
    shipDate = Column(DateTime)
    amount = Column(Integer)

    medicine = relationship("Medicine")
    user = relationship("User")


class Medicine(Base):
    __tablename__ = 'medicine'
    id_medicine = Column(Integer, primary_key=True)
    name = Column(String(45))
    manufacturer = Column(String(45))
    price = Column(Integer)
    in_stock = Column(Boolean)
    demand = Column(Boolean)
    in_stock_number = Column(Integer)
    demand_number = Column(Integer)
