import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Deck, Card


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def greeting():
        return 'Welcome to Magic: The Gathering API'

    @app.route('/decks')
    def get_decks():
        decks = Deck.query.all()
        decks_readable = [
            f'{deck.title} by {deck.creator}' for deck in decks]

        return jsonify(decks_readable)

    @app.route('/cards')
    def get_cards():
        cards = Card.query.all()
        cards_readable = [
            f'{card.name}' for card in cards]

        return jsonify(cards_readable)

    @app.route('/cards', methods=['post'])
    def post_card():
        data = json.loads(request.data)
        name = data.get('name', None)
        type = data.get('type', None)
        colors = data.get('colors', None)
        cmc = data.get('cmc', None)

        try:
            new_card = Card(name, type, colors, cmc)
            new_card.insert()
        except Exception as e:
            print('There was an exception:')
            print(e)
            abort(422)

        return 'posted card successfully'

    @app.route('/cards/<int:id>', methods=['patch'])
    def update_card(id):
        try:
            working_card = Card.query.get(id)
        except Exception as e:
            print(f'There was an exception:\n{e}')
            abort(404)

        try:
            data = json.loads(request.data)
            name = data.get('name', None)
            type = data.get('type', None)
            colors = data.get('colors', None)
            cmc = data.get('cmc', None)
        except Exception as e:
            print(f'There was an exception:\n{e}')
            abort(400)

        try:
            if name:
                working_card.name = name
            if type:
                working_card.type = type
            if colors:
                working_card.colors = colors
            if cmc:
                working_card.cmc = cmc
            working_card.update()
        except Exception as e:
            print(f'There was an exception:\n{e}')
            abort(422)

        return f'updated card successfully: {working_card.name} - {working_card.type} - {working_card.colors} - {working_card.cmc}'

    @app.route('/cards/<int:id>', methods=['delete'])
    def delete_card(id):
        try:
            working_card = Card.query.get(id)
            test = working_card.id
        except Exception as e:
            print(f'There was an exception:\n{e}')
            abort(404)

        try:
            working_card.delete()
        except Exception as e:
            print(f'There was an exception:\n{e}')
            abort(422)

        return f'deleted card successfully: {working_card.id} - {working_card.name}'

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
