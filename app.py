import json
import os
import requests
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from livereload import Server


from auth import requires_auth
from models import setup_db, Deck, Card


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)

    @app.route('/')
    # @requires_auth()
    def greeting():
        """Routes user to a welcome page."""
        random_card = requests.get('https://api.scryfall.com/cards/random').json()
        print('hello')
        print(random_card)

        return render_template('home.html')
        # return 'Welcome to Magic: The Gathering API'

    @app.route('/contact')
    def contact_page():
        """Routes user to contact info page."""

        return render_template('contact.html') 

    @app.route('/decks')
    @requires_auth('get:decks')
    def get_decks():
        """
        Displays all the decks. 
        An mtg_browser or mtg_publisher role is needed.
        """

        decks = Deck.query.all()
        decks_readable = [
            f'{deck.title} by {deck.creator}' for deck in decks]

        return jsonify(decks_readable)

    @app.route('/cards')
    @requires_auth('get:cards')
    def get_cards():
        """
        Displays all the cards. 
        An mtg_browser or mtg_publisher role is needed.
        """

        cards = Card.query.all()
        cards_readable = [
            f'{card.name}' for card in cards]

        return jsonify(cards_readable)

    @app.route('/cards', methods=['post'])
    @requires_auth('post:cards')
    def post_card():
        """
        Allows a user to post a new card to the database.

        The user must supply a JSON body in their post request as well as a 
        valid JWT in the header. The JSON body must contain "name" and 
        "type", and it can optionally contain "colors" and "cmc". 
        An mtg_publisher role is needed.
        """

        data = json.loads(request.data)
        name = data.get('name')
        type = data.get('type')
        colors = data.get('colors')
        cmc = data.get('cmc')

        try:
            new_card = Card(name, type, colors, cmc)
            new_card.insert()
        except Exception as e:
            print('There was an exception:')
            print(e)
            abort(422)

        return jsonify('posted card successfully')

    @app.route('/cards/<int:id>', methods=['patch'])
    @requires_auth('patch:cards')
    def update_card(id):
        """
        Allows a user to patch an existing card in the database.

        The user must indicate which card they want to edit by providing an id. 
        They must also supply a JSON body in their patch request as well as a 
        valid JWT in the header. The JSON body should contain key:value pairs 
        for the card attribtutes the user would like to update. 
        An mtg_publisher role is needed.
        """

        try:
            working_card = Card.query.get(id)
            test = working_card.id
        except Exception as e:
            print(f'There was an exception:\n{e}')
            abort(404)

        try:
            data = json.loads(request.data)
            name = data.get('name')
            type = data.get('type')
            colors = data.get('colors')
            cmc = data.get('cmc')
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

        return f"""
        updated card successfully: {working_card.name} - 
        {working_card.type} - {working_card.colors} - 
        {working_card.cmc}
        """

    @app.route('/cards/<int:id>', methods=['delete'])
    @requires_auth('delete:cards')
    def delete_card(id):
        """
        Allows a user to delete a card from the database.

        The user must indicate which card they want to delete by providing 
        an id. They must also supply a valid JWT in the header.
        An mtg_publisher role is needed.
        """

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

        return f"""
        deleted card successfully: 
        {working_card.id} - {working_card.name}
        """

    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "the client sent a bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "user is not authorized to access this resource"
        }), 401

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "the request method is not allowed on this resource"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "the request was unprocessable"
        }), 422

    return app


app = create_app()

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(host='localhost', port=8080, debug=True)
    server = Server(app.wsgi_app)
    server.watch('/Users/david/Documents/Programming/Udacity/Full_Stack_Developer/Unit_6-Capstone/mtg-api/')
    server.serve()
