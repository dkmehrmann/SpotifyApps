from flask import Flask, request, redirect, g, render_template, session, url_for
from spotifyAPI import auth, playlists
import requests

application = Flask(__name__)
application.secret_key = 'some key for session'

# ----------------------- AUTH API PROCEDURE -------------------------

@application.route("/auth")
def autho():
    return redirect(auth.AUTH_URL)


@application.route("/callback/")
def callback():

    auth_token = request.args['code']
    auth_header = auth.authorize(auth_token)
    session['auth_header'] = auth_header

    return redirect(url_for("index"))


@application.route("/logout")
def logout():
    session.pop('auth_header')

    return _playlists()


def valid_token(resp):

    return resp is not None and not 'error' in resp


# ----------------------- Actual Requests -------------------------

@application.route('/')
@application.route('/index')
def index():

    if 'auth_header' in session:
        auth_header = session['auth_header']
        resp = requests.get("https://api.spotify.com/v1/me", headers=auth_header)
        return render_template('index.html', resp=resp.json())

    return render_template('index.html')


@application.route('/playlists')
def _playlists():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        playlist_data, code = playlists.get_playlist_songs(auth_header)

        if code == 401:
            print('hit redirect for token')
            return redirect(auth.AUTH_URL)

        playlist_data = playlists.add_accused(playlist_data)

        return render_template("playlists.html", resp=playlist_data)

    return render_template('playlists.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
