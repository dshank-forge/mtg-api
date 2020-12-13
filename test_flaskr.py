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
        self.database_path = 'postgres://localhost:5432/magic_the_gathering_test'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        print('Test Complete.')

    def test_get_decks(self):
        response = self.client.get('/decks')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_405_patch_decks(self):
        response = self.client.patch('/decks')

        self.assertEqual(response.status_code, 405)

    def test_get_cards(self):
        response = self.client.get('/cards')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_405_delete_cards(self):
        response = self.client.delete('/cards')

        self.assertEqual(response.status_code, 405)

    def test_post_card(self):
        name = 'Tarmogoyf'
        type = 'Creature'
        colors = 'Green'
        cmc = 2

        card_json = {"name": name, "type": type, "colors": colors, "cmc": cmc}
        response = self.client.post("/cards", json=card_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data), 'posted card successfully')

    def test_422_post_incomplete_card(self):
        name = None
        type = 'Enchantment'
        colors = 'White'
        cmc = 4

        card_json = {"name": name, "type": type, "colors": colors, "cmc": cmc}
        response = self.client.post("/cards", json=card_json)

        self.assertEqual(response.status_code, 422)

    def test_patch_card(self):
        colors = 'colorless'

        card_json = {"colors": colors}
        response = self.client.patch("/cards/17", json=card_json)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(colors in str(response.data))
        self.assertTrue('updated card successfully' in str(response.data))

    def test_404_patch_non_existent_card(self):
        colors = 'white-blue-red'
        cmc = 3

        card_json = {"colors": colors, "cmc": cmc}
        response = self.client.patch("/cards/900", json=card_json)

        self.assertEqual(response.status_code, 404)

    def test_delete_card(self):
        response = self.client.delete("/cards/1")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('deleted card successfully: 1 -' in str(response.data))

    def test_404_delete_non_existent_card(self):
        response = self.client.delete("/cards/900")

        self.assertEqual(response.status_code, 404)

    # TODO: Build a couple tests to test RBAC.


if __name__ == "__main__":
    unittest.main()
