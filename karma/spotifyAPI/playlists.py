from config import SPOTIFY_API_URL
import requests
from accused import accused_artists
from flask import redirect
from spotifyAPI import auth

def safe_GET(url, auth_header, **kwargs):
    resp = requests.get(url, headers=auth_header, **kwargs)

    if resp.status_code == 401:
        redirect(auth.AUTH_URL)

    return resp.json()


def get_playlists(auth_header):

    USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
    USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
    resp = requests.get(USER_PLAYLISTS_ENDPOINT, headers=auth_header)

    # ADD PAGINATION HERE

    return resp.json(), resp.status_code


def get_songs(auth_header, plist_id):
    # https: // api.spotify.com / v1 / playlists / {playlist_id} / tracks

    URL = "{}/playlists/{}/tracks".format(SPOTIFY_API_URL, plist_id)

    params = {"fields": "items(track(name, uri, id, artists))"}

    resp = requests.get(URL, headers=auth_header, params=params)

    # ADD PAGINATION HERE

    return resp.json(), resp.status_code


def get_playlist_songs(auth_header):

    plists, code = get_playlists(auth_header)

    if code != 200:
        return {}, code

    for x in plists['items']:
        x['songs'], code = get_songs(auth_header, x['id'])

        if code != 200:
            return plists, code

    return plists, 200


def add_accused(plists):

    for plist in plists['items']:
        for song in plist['songs']['items']:
            song['is_accused'] = False
            for artist in song['track']['artists']:
                if artist['name'] in accused_artists:
                    song['is_accused'] = True
                    break

    return plists

