Motivation:
My motivation for building this API was to combine two of my passions: coding and Magic: the Gathering. 
This API shares some of my favorite cards and decks from Magic.

Setup Instructions:
To install dependencies, run "pip install -r requirements.txt". Then run "source setup.sh" to export environment variables.
To launch the app locally, run "flask run --reload". To execute unit tests, run "source run_tests.sh". If you run the app 
locally, it will be available at: http://127.0.0.1:5000/. If you wish to create a local database with some test data, 
you can run "createdb (YOUR_DB_NAME)" and then "psql (YOUR_DB_NAME) < test_db.pgsql".

The deployed Heroku app can be found at: https://magic-the-gathering-api.herokuapp.com/

Roles:
mtg_browser: can view cards and decks
mtg_publisher: can view cards and decks, and can also create, delete, and edit individual cards

Authentication instructions: 
Pre-generated JWTs for each user-role can be found in the setup.sh file. You can use these with Curl or Postman to 
access the API endpoints. Please run "source setup.sh" once to export these JWTs as environment variables so that 
unit tests can be run locally. If you wish to generate your own JWT, you can visit the Auth0 login URL below. 
Please note that by using this method to sign in, you will receive a generic JWT without any associated role. It
will therefore only be able to access the index endpoint.

Auth0 Login URL: 
https://goatpig.us.auth0.com/login?state=g6Fo2SBXcmwtNFFXNDJ4WEhXUS01VzVxMmtUNGRDSTVwTnJaVqN0aWTZIEpLYi04N2E5a0s3OWU1RDh3SGE5NG95NWpnaXhabmNIo2NpZNkgRWJJb2pGRmlRelM3VWsxMWUxSTZUYjVzNXkyckt6WEg&client=EbIojFFiQzS7Uk11e1I6Tb5s5y2rKzXH&protocol=oauth2&audience=mtg&response_type=token&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2F

---API Documentation---
Endpoints: 
GET '/cards'
GET '/decks'
POST '/cards'
PATCH '/cards/{id}'
DELETE '/cards/{id}'

GET '/cards'
- Fetches all cards in the database.
- Request Arguments: None
- Returns: A list of cards
[
    "snapcaster mage",
    "lightning bolt",
    "emrakul, the aeons torn",
    "grim flayer",
    "lashweed lurker",
    "glimmer of genius",
    "botanical sanctum",
    "Tarmogoyf",
    "Mana Confluence",
    "sylvan library"
]

GET '/decks'
- Fetches all decks in the database.
- Request Arguments: None
- Returns: A list of decks, each with a well-known pilot
[
    "jund by reid duke",
    "esper dragons by shota yasooka"
]

POST '/cards'
- Posts a new card to the database based on the JSON body of the request
- Request Arguments: None
- Returns: A message telling the user that card has been posted successfully
Request Body:
{
    "name": "forest",
    "type": "land",
    "colors": "colorless",
    "cmc": 0
}
Response:
"posted card successfully"

PATCH '/cards/{id}'
- Updates an existing card based on the JSON body of the request
- Request Arguments: None
- Returns: A message telling the user that card has been updated, along with
the updated details of that card
Request Body sent to '/cards/3':
{"cmc": 4}
Response:
updated card successfully: polymorph - sorcery - blue - 4

DELETE '/cards/{id}'
- Deletes a card from the database
- Request Arguments: None
- Returns: A message telling the user that the card has been deleted, along with
details about what card was deleted.
Response:
deleted card successfully: 4 - polymorph

