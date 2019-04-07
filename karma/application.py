from flask import Flask, request, redirect, render_template, session, url_for, jsonify
from spotifyAPI import auth, playlists
import requests
from requests import exceptions

application = Flask(__name__)
application.secret_key = 'some key for session'


def handle_error(e):

    return render_template('index.html', resp={'error': {'msg': e.strerror, 'code': e.errno}})


# ----------------------- AUTH API PROCEDURE -------------------------

@application.route("/auth")
def autho():
    return redirect(auth.AUTH_URL)


@application.route("/callback/")
def callback():

    auth_token = request.args['code']
    auth_header = auth.authorize(auth_token)
    session['auth_header'] = auth_header

    resp = requests.get("https://api.spotify.com/v1/me", headers=auth_header)
    session['user_data'] = resp.json()

    return redirect(url_for("index"))


@application.route("/logout")
def logout():

    if 'auth_header' in session:
        session.pop('auth_header')
    if 'user_data' in session:
        session.pop('user_data')

    return redirect(url_for("index"))


# ----------------------- Actual Requests -------------------------

@application.route('/')
@application.route('/index')
def index():

    if 'auth_header' in session and 'user_data' in session:

        return render_template('index.html', resp=session['user_data'])

    return render_template('index.html', resp={'error':'please log in to continue'})


@application.route('/playlists', methods=['GET', 'POST'])
def _playlists():
    if 'auth_header' in session and 'user_data' in session:
        auth_header = session['auth_header']

        if request.method == "GET":

            try:
                playlist_data = playlists.get_all_user_songs(auth_header)
                # session['user_playlists'] = playlist_data
            except exceptions.HTTPError as e:
                return handle_error(e)


            return render_template("playlists.html", resp=playlist_data,
                                   title='Tracks and Artists in your Playlists and Library')

        if request.method == "POST":
            artist_list = request.form.getlist('artists')
            # playlist_data = session['user_playlists']

            for plist in playlist_data['items']:
                songlist = plist['songs']['items']
                songlist = [x for x in songlist if len(set(x['track']['artists']) & set(artist_list)) > 0]
                plist['songs']['items'] = songlist

            return render_template("playlists.html", resp=playlist_data,
                                   title='Tracks and Artists in your Playlists and Library')


    return redirect(url_for("index"))


@application.route('/playlists/accused', methods=['GET', 'POST'])
def _accused():
    if 'auth_header' in session and 'user_data' in session:
        auth_header = session['auth_header']

        # try:
        #     playlist_data = playlists.get_all_user_songs(auth_header)
        # except exceptions.HTTPError as e:
        #     return handle_error(e)

        # playlist_data = playlists.add_accused(playlist_data)

        # for plist in playlist_data['items']:
        #     songlist = plist['songs']['items']
        #     songlist = [x for x in songlist if x['is_accused']==True]
        #     plist['songs']['items'] = songlist

        if request.method == "POST":
            thing = request.form.getlist('artists')

            return jsonify(thing)
        return render_template("playlists.html", resp=playlist_data,
                               title='Accused Artists in your Playlists and Library')

    return redirect(url_for("index"))


@application.route('/test')
def _testendpoint():
    from flask import jsonify
    if 'auth_header' in session and 'user_data' in session:
        auth_header = session['auth_header']

        playlist_data = playlists.get_playlists(auth_header)

        return jsonify(playlist_data)

    return render_template('playlists.html')


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()