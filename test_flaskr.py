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
        self.mtg_browser_jwt = os.environ.get('MTG_BROWSER_JWT')
        self.mtg_publisher_jwt = os.environ.get('MTG_PUBLISHER_JWT')
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        print('Test Complete.')

    # Test all endpoints using an mtg_publisher role

    def test_get_index(self):
        response = self.client.get(
            '/', headers={"Authorization": f"Bearer {self.mtg_publisher_jwt}"})

        self.assertEqual(response.status_code, 200)

    def test_401_get_index_bad_jwt(self):
        response = self.client.get(
            '/', headers={"Authorization": "Bearer fake-token"})

        self.assertEqual(response.status_code, 401)

    def test_get_decks(self):
        response = self.client.get(
            '/decks',
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_405_patch_decks(self):
        response = self.client.patch(
            '/decks',
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            })

        self.assertEqual(response.status_code, 405)

    def test_get_cards(self):
        response = self.client.get(
            '/cards',
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_405_delete_cards(self):
        response = self.client.delete(
            '/cards',
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            })

        self.assertEqual(response.status_code, 405)

    def test_post_card(self):
        name = 'Tarmogoyf'
        type = 'Creature'
        colors = 'Green'
        cmc = 2

        card_json = {"name": name, "type": type, "colors": colors, "cmc": cmc}
        response = self.client.post(
            "/cards",
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            },
            json=card_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(data), 'posted card successfully')

    def test_422_post_incomplete_card(self):
        name = None
        type = 'Enchantment'
        colors = 'White'
        cmc = 4

        card_json = {"name": name, "type": type, "colors": colors, "cmc": cmc}
        response = self.client.post(
            "/cards",
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            },
            json=card_json)

        self.assertEqual(response.status_code, 422)

    def test_patch_card(self):
        colors = 'colorless'

        card_json = {"colors": colors}
        response = self.client.patch(
            "/cards/17",
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            },
            json=card_json)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(colors in str(response.data))
        self.assertTrue('updated card successfully' in str(response.data))

    def test_404_patch_non_existent_card(self):
        colors = 'white-blue-red'
        cmc = 3

        card_json = {"colors": colors, "cmc": cmc}
        response = self.client.patch(
            "/cards/900",
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            },
            json=card_json)

        self.assertEqual(response.status_code, 404)

    def test_delete_card(self):
        response = self.client.delete(
            "/cards/1",
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('deleted card successfully:' in str(response.data))

    def test_404_delete_non_existent_card(self):
        response = self.client.delete(
            "/cards/900",
            headers={
                "Authorization":
                f"Bearer {self.mtg_publisher_jwt}"
            })

        self.assertEqual(response.status_code, 404)

    # Test a couple of endpoints with the mtg_browser role

    def test_get_decks_mtg_browser(self):
        response = self.client.get(
            '/decks',
            headers={
                "Authorization":
                f"Bearer {self.mtg_browser_jwt}"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_get_cards_mtg_browser(self):
        response = self.client.get(
            '/cards',
            headers={
                "Authorization":
                f"Bearer {self.mtg_browser_jwt}"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_401_delete_card_mtg_browser(self):
        response = self.client.delete(
            "/cards/2", headers={
                "Authorization":
                f"Bearer {self.mtg_browser_jwt}"
            })

        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
