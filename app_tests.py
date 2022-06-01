from unittest import TestCase, main
from unittest.mock import ANY

import sqlalchemy

from app import app
from constants import *
from model import *
import shm
import bcrypt
import json
from flask import url_for
from base64 import b64encode

app.testing = True
client = app.test_client()


class BaseTestCase(TestCase):
    client = app.test_client()

    def setUp(self):
        super().setUp()

        # Users and admins data
        self.user_1_data = {
            "firstName": "Ivan",
            "lastName": "Petrenko",
            "email": "ivan@com",
            "phone": "056235623",
            "login": "user1",
            "password": "user1",
            "is_provisor": False,
        }
        self.user_1_data_hashed = {
            **self.user_1_data,
            "password": bcrypt.hashpw(bytes(self.user_1_data['password'], 'utf-8'), bcrypt.gensalt())
        }
        self.user_1_credentials = b64encode(b"user1:user1").decode('utf-8')

    def clear_user_db(self):
        engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from user;')

    def create_all_users(self):
        self.client.post('api/v15/user', json=self.user_1_data)

class TestUser(BaseTestCase):
    def test_create_user_1(self):
        self.clear_user_db()
        response = self.client.post('/api/v1/User', json=self.user_1_data)
        self.assertEqual(response.status_code, 201)

