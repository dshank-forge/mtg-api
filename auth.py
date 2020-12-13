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

print('we are in bizness')


# Get the JWT from the Authorization header


def get_token_auth_header():
    try:
        headers = request.headers
        auth_part = headers['Authorization']
        split_auth_part = auth_part.split()
        bearer = split_auth_part[0]
        token = split_auth_part[1]
    except Exception as e:
        print(f'There was an exception:\n{e}')
        abort(401)
    return token


# Check if the permission is in the payload


def check_permissions(permission, payload):
    try:
        permissions_array = payload['permissions']
        # print('permissions array: ' + str(permissions_array))
        # print('permission:' + str(permission))
        if permission not in permissions_array:
            raise Exception(
                'The specified permission is not in this permission set.')
    except Exception as e:
        print(f'There was an exception:\n{e}')
        abort(401)
    return True


# The following function has been adapted from the Auth0 Docs - "Python API: Authorization" by Luciano Balmaceda
# URL: https://auth0.com/docs/quickstart/backend/python/01-authorization?_ga=2.212761047.219893380.1606509180-267051542.1604770864#create-the-jwt-validation-decorator
# Date: 12/13/2020

# ----- Begin Citation ----- #


def create_verification_key(jwks_dict, token):
    unverified_header = jwt.get_unverified_header(token)

    for key in jwks_dict["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break

    return rsa_key


# ----- End Citation ----- #


# Verify and decode the JWT. Return the payload.

def verify_decode_jwt(token):
    jwks_dictionary = json.loads(
        urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json').read())

    try:
        verification_key = create_verification_key(jwks_dictionary, token)
    except Exception as e:
        print(f'There was an exception:\n{e}')
        abort(401)

    try:
        payload = jwt.decode(token, verification_key, algorithms=ALGORITHMS,
                             audience=API_AUDIENCE)
    except Exception as e:
        print(f'There was an exception:\n{e}')
        abort(401)

    return payload
