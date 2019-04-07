from config import SPOTIFY_API_URL
import requests
from accused import accused_artists
from flask import session
from requests import exceptions

def safe_GET(url, **kwargs):

    resp = requests.get(url, **kwargs)

    if resp.status_code != 200:
        raise exceptions.HTTPError(resp.status_code, "error from spotify client")

    return resp


def paginated_GET(url, page_size, **kwargs):

    y = {'limit': page_size, 'offset': 0}

    if 'params' in kwargs:
        params = kwargs.pop("params")
        params = {**params, **y}
    else:
        params = y

    resp = safe_GET(url, params=params, **kwargs)
    temp = resp.json()
    params['offset'] += page_size

    while params['offset'] < resp.json()['total']:
        resp = safe_GET(url, params=params, **kwargs)
        temp['items'].extend(resp.json()['items'])
        params['offset'] += page_size

    return temp


def get_playlists(auth_header):

    USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
    USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
    plists = paginated_GET(USER_PLAYLISTS_ENDPOINT, page_size=50, headers=auth_header)

    filtered = [x for x in plists['items'] if x['owner']['uri'] == session['user_data']['uri']]

    plists['items'] = filtered

    return plists


def get_playlist_songs(auth_header, plist_id):
    # https: // api.spotify.com / v1 / playlists / {playlist_id} / tracks

    URL = "{}/playlists/{}/tracks".format(SPOTIFY_API_URL, plist_id)

    params = {"fields": "items(track(name, uri, id, artists)), total, limit"}

    resp = paginated_GET(URL, page_size=100, headers=auth_header, params=params)

    return resp


def get_library(auth_header):

    URL = "{}/me/tracks".format(SPOTIFY_API_URL)
    params = {"fields": "items(track(name, uri, id, artists))"}
    resp = paginated_GET(URL, page_size=50, headers=auth_header, params=params)

    return resp

def get_all_user_songs(auth_header):

    plists = get_playlists(auth_header)

    for x in plists['items']:
        x['songs'] = get_playlist_songs(auth_header, x['id'])

    ulib = {'name': 'User Library (saved tracks)', 'songs': get_library(auth_header)}

    plists['items'] = [ulib] + plists['items']

    return plists

'''
def add_accused(plists):

    for plist in plists['items']:
        for song in plist['songs']['items']:
            song['is_accused'] = False
            for artist in song['track']['artists']:
                if artist['name'] in accused_artists:
                    song['is_accused'] = True
                    break

    return plists
'''