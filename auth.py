import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt, exceptions
from urllib.request import urlopen

AUTH0_DOMAIN = 'goatpig.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'mtg'
CLIENT_SECRET = 'oues1xfgBTGViGZTZApPnNsRNoZ59bzQX44blRAuV-apyBBWoyGTrG8TKxF2sVwD'

# Auth0 login:
# 'https://goatpig.us.auth0.com/authorize?audience=mtg&response_type=token&client_id=EbIojFFiQzS7Uk11e1I6Tb5s5y2rKzXH&redirect_uri=https://127.0.0.1:5000/'
