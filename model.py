from sqlalchemy import create_engine, Integer, String, Column, Date, ForeignKey, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, Date, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

<<<<<<< HEAD
engine = create_engine('mysql+pymysql://root:PavloVasylevych@localhost:3306/mydb')
=======
engine = create_engine('mysql+pymysql://root:OlehSyniuk@localhost:3306/pp')
>>>>>>> origin/main

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'
    id=Column(Integer, primary_key=True)
    name=Column(String(45))
    surname=Column(String(45))
<<<<<<< HEAD
    username=Column(String(45))
    password=Column(String(45))

class Audience(Base):
    __tablename__ = 'audience'
    id = Column(Integer, primary_key=True)
    number=Column(Integer)
    amount_of_places=Column(Integer)
    status=Column(Boolean)
    reservuation_date=Column(Date)

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title=Column(String(45))
    audience_id = Column(Integer, ForeignKey('audience.id'))
    date = Column(Date)
    audience = relationship("Audience")
    user = relationship("User")
=======
    login=Column(String(45))
    password=Column(String(45))

class Purchase(Base):
    __tablename__ = 'Purchase'
    id = Column(Integer, primary_key=True)
    total_cost=Column(Integer)
    user_id=Column(Integer)
    medicine_id=Column(Integer)

class Medicine(Base):
    __tablename__ = 'Medicine'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    expiration_date = Column(Date)
    cost = Column(Integer)
>>>>>>> origin/main
