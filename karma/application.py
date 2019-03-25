from flask import Flask, request, redirect, g, render_template, session, url_for
from spotifyAPI import auth, playlists

app = Flask(__name__)
app.secret_key = 'some key for session'

# ----------------------- AUTH API PROCEDURE -------------------------

@app.route("/auth")
def autho():
    return redirect(auth.AUTH_URL)


@app.route("/callback/")
def callback():

    auth_token = request.args['code']
    auth_header = auth.authorize(auth_token)
    session['auth_header'] = auth_header

    return redirect(url_for("_playlists"))


@app.route("/logout")
def logout():
    session.pop('auth_header')

    return _playlists()


def valid_token(resp):

    return resp is not None and not 'error' in resp


# ----------------------- Actual Requests -------------------------

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/playlists')
def _playlists():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        playlist_data = playlists.list_songs(auth_header)

        playlist_data = playlists.add_accused(playlist_data)

        return render_template("playlists.html", resp=playlist_data)

    return render_template('playlists.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()