import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Card, Deck


class MtgTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_path = 'postgres://localhost:5432/magic_the_gathering'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        print('Test Complete.')

    def test_get_cards(self):
        response = self.client().get('/cards')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
