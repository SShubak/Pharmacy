import unittest
from unittest import TestCase, main
from unittest.mock import ANY
import sqlalchemy
from sqlalchemy import delete

from app import app
from constants import *
from model import *
from shm import *
import bcrypt
import json
from flask import url_for
from base64 import b64encode



app.testing = True
client = app.test_client()


class Tests(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    tester = app.test_client()
    s = Session()


    def setUp(self):
        delete()

    def tearDown(self):
        self.close_session()

    def close_session(self):
        self.s.close()

class TestUser(Tests):

    user = {
        "firstName": "Oleh",
        "lastName": "Syniuk",
        "email": "oleh@com",
        "phone": "2352351135",
        "login": "o-leg",
        "password": "123456",
        "is_provisor": "0"
    }

    data2 = {
        "firstName": "Olehhh",
        "lastName": "Syniukkk",
        "email": "oleh@commm",
        "phone": "235235113555",
        "login": "o-leggg",
        "password": "12345666",
        "is_provisor": "0"
    }

    data_put = {
        "firstName": "Oleleh",
        "lastName": "Syniukkk",
        "email": "oleleh@commm",
        "phone": "235235113555",
        "login": "o-leleggg",
        "password": "12345666",
        "is_provisor": "0"
    }

    data_put_wr = {
        "firstName": "Olehhh-Oleh",
        "lastName": "Syniukkk-o",
        "email": "oleh@commm0com",
        "phone": "235235113555",
        "login": "o-legggh",
        "password": "12345666",
        "is_provisor": "0"
    }

    def test_post_user_200(self):
        delete()
        response = self.tester.post("/api/v1/User", data=json.dumps(self.user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_post_user_400(self):
        delete()
        response = self.tester.post("/api/v1/User", data=json.dumps(self.data2),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)


    def test_get_user_by_id_200(self):
        delete()
        user = User(id_user=3, firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        self.s.add(user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.get("/api/v1/getuser/3", headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({"user": {"id": 3, "firstName": "Oleh", "lastName": "Syniuk", "login": "o-leg"}}, response.json)

    def test_get_user_by_id_404(self):
        delete()
        user = User(firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        self.s.add(user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.get("/api/v1/getuser/100", headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 404)

    def test_get_user_by_id_405(self):
        delete()
        user = User(firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        add_user = User(id_user="5", firstName="test", lastName="test", login="oleleg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        Session().add(user)
        Session().commit()
        self.s.add(user)
        self.s.add(add_user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.get("/api/v1/getuser/5", headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 405)

    def test_put_user_200(self):
        delete()
        user = User(id_user="3", firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        self.s.add(user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.put("/api/v1/updateuser/3", data=json.dumps(self.data_put), content_type="application/json",
                                   headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 200)

    def test_put_user_404(self):
        delete()
        user = User(id_user="3", firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        add_user = User(firstName="test", lastName="test", login="o-leleg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        self.s.add(user)
        self.s.add(add_user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.put("/api/v1/updateuser/3", data=json.dumps(self.data_put_wr), content_type="application/json",
                                   headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 404)

    def test_del_user(self):
        delete()
        user = User(id_user="3", firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        self.s.add(user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.delete("/api/v1/deleteuser/3", headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 200)

    def test_del_user_404(self):
        user = User(id_user="3", firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        self.s.add(user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.delete("/api/v1/deleteuser/4", headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 404)

    def test_del_user_405(self):
        delete()
        user = User(id_user="3", firstName="Oleh", lastName="Syniuk", login="o-leg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        add_user = User(id_user="4", firstName="test", lastName="test", login="o-legg",
                    password="123456", email="oleh@com", phone="2352351135", is_provison="0")
        self.s.add(user)
        self.s.add(add_user)
        self.s.commit()
        us = b64encode(b"o-leg:123456").decode("utf-8")
        response = self.tester.delete("/api/v1/deleteuser/4", headers={"Authorization": f"Basic {us}"})
        self.assertEqual(response.status_code, 405)

