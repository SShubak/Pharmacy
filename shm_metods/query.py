from sqlalchemy.orm import sessionmaker

from shm_metods.model import User, Purchase, Medicine, engine
from shm_metods.model import Session

session = sessionmaker(bind = engine)
s = Session()

user = User(name="guy", surname="boy", login="test", password="12345678")
user1 = User(name="girl", surname="ntt", login="nottest", password="12345678")
medicine = Medicine(name="Galvadol", expiration_date='2021-10-21')
medicine1 = Medicine(name="Balalol", expiration_date='2023-06-15')
purchase = Purchase(total_cost=5432, user_id=1, medicine_id=1)
purchase1 = Purchase(total_cost=12345, user_id=2, medicine_id=2)

s.add(user)
s.add(medicine)
s.add(user1)
s.add(medicine1)

s.commit()

s.add(purchase)
s.add(purchase1)

s.commit()

s.close()
