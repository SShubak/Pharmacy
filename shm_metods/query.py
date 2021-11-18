from sqlalchemy.orm import sessionmaker

from shm_metods.model import User, Order, Medicine, engine
from shm_metods.model import Session

session = sessionmaker(bind = engine)
s = Session()

user = User(id_user=1, firstName="guy", lastName="boy", login="test", password="12345678", email="afawfawf@gmail.com", phone="380508832580")
user1 = User(id_user=2, firstName="girl", lastName="ntt", login="nottest", password="12345678", email="qwertyf@gmail.com", phone="380508832581")
medicine = Medicine(id_medicine=1, name="Galvadol", manufacturer="Ukraine", price=100, in_stock=True, demand=False, in_stock_number=20, demand_number=0)
medicine1 = Medicine(id_medicine=2, name="Balalol", manufacturer="Ukraine", price=100, in_stock=True, demand=False, in_stock_number=20, demand_number=0)
order = Order(id_order=1, id_medicine=1, id_user=1, shipDate="2021-11-17", amount=10, status="approved")
order1 = Order(id_order=2, id_medicine=2, id_user=2, shipDate="2021-11-17",amount=5 , status="placed")

s.add(user)
s.add(medicine)
s.add(user1)
s.add(medicine1)
s.add(order)
s.add(order1)

s.commit()

