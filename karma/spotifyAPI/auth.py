from config import SCOPE, SPOTIFY_AUTH_URL, REDIRECT_URI, SPOTIFY_TOKEN_URL
import urllib
from credentials import CLIENT_ID, CLIENT_SECRET
import requests
import json
import base64

# ----------------- 1. USER AUTHORIZATION ----------------


# STATE = ""
# SHOW_DIALOG_bool = True
# SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# https://developer.spotify.com/web-api/authorization-guide/
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, urllib.parse.urlencode(auth_query_parameters))


def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}

    return auth_header
