# URLS
import os

SPOTIFY_API_URL = 'https://api.spotify.com/v1'
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')


SCOPE = "playlist-modify-public playlist-modify-private playlist-read-collaborative playlist-read-private user-library-read"


# need to register this in spotify dev console

CLIENT_SIDE_URL = os.getenv("MYHOSTNAME")

REDIRECT_URI = "{}/callback/".format(CLIENT_SIDE_URL)
print(REDIRECT_URI)

