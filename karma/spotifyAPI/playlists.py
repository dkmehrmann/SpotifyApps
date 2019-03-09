from karma.config import SPOTIFY_API_URL
import requests




def get_playlists(auth_header):

    USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
    USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
    resp = requests.get(USER_PLAYLISTS_ENDPOINT, headers=auth_header)

    return resp.json()

def list_playlists(auth_header):

    resp = get_playlists(auth_header)

    out = []

    for plist in resp['items']:
        out.append({"name": plist['name'], "id": plist['id']})

    return out


def get_songs(auth_header, plist_id):
    # https: // api.spotify.com / v1 / playlists / {playlist_id} / tracks

    URL = "{}/playlists/{}/tracks".format(SPOTIFY_API_URL, plist_id)

    params = {"fields": "items(track(name, uri, id, artists))"}

    resp = requests.get(URL, headers=auth_header, params=params)

    return resp.json()


def list_songs(auth_header):

    plists = list_playlists(auth_header)

    for x in plists:
        x['songs'] = get_songs(auth_header, x['id'])

    return plists

