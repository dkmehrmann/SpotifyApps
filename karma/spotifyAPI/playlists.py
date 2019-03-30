from config import SPOTIFY_API_URL
import requests
from accused import accused_artists
from flask import redirect
from spotifyAPI import auth

def safe_GET(url, **kwargs):
    resp = requests.get(url, **kwargs)

    if resp.status_code == 401:
        redirect(auth.AUTH_URL)

    return resp


def get_playlists(auth_header):

    USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
    USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
    resp = safe_GET(USER_PLAYLISTS_ENDPOINT, headers=auth_header)

    # ADD PAGINATION HERE

    return resp.json()


def get_songs(auth_header, plist_id):
    # https: // api.spotify.com / v1 / playlists / {playlist_id} / tracks

    URL = "{}/playlists/{}/tracks".format(SPOTIFY_API_URL, plist_id)

    params = {"fields": "items(track(name, uri, id, artists))"}

    resp = safe_GET(URL, headers=auth_header, params=params)

    # ADD PAGINATION HERE

    return resp.json()


def get_playlist_songs(auth_header):

    plists = get_playlists(auth_header)

    for x in plists['items']:
        x['songs'] = get_songs(auth_header, x['id'])

    return plists


def add_accused(plists):

    for plist in plists['items']:
        for song in plist['songs']['items']:
            song['is_accused'] = False
            for artist in song['track']['artists']:
                if artist['name'] in accused_artists:
                    song['is_accused'] = True
                    break

    return plists

