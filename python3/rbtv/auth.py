import os
import json

tokens = os.path.join(os.path.dirname(__file__), '..', '..', 'tokens.json')

token = ''
refreshToken = ''

with open(tokens) as f:
    d = json.load(f)
    token = d.get('token', '*** REMOVED ***')
    refreshToken = d.get('refreshToken', '*** REMOVED ***')

def saveNewToken(aToken):
    token = aToken
    with open(tokens, 'w') as outfile:
        json.dump({'token':aToken, 'refreshToken':refreshToken}, outfile)
