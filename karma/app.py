from flask import Flask, request, redirect, g, render_template, session
from karma.spotifyAPI import auth, playlists

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

    return profile()

@app.route("/logout")
def logout():
    session.pop('auth_header')

    return profile()

def valid_token(resp):

    return resp is not None and not 'error' in resp


# ----------------------- Actual Requests -------------------------

@app.route('/index')
def profile():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        playlist_data = playlists.list_songs(auth_header)

        return render_template("index.html", resp=playlist_data)

    return render_template('index.html')