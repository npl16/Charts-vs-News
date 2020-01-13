#Adapated from Flask-Spotify-Auth code by Greg Van Ort available at https://github.com/vanortg/Flask-Spotify-Auth

from flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "b585cb9e4584453ca897923691da4405"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "" #Key redacted for security

#Port and callback url can be changed or ledt to localhost:5000
PORT = ""
CALLBACK_URL = "http://npl16.pythonanywhere.com"

#Add needed scope from spotify user
SCOPE = "playlist-modify-public user-read-private"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}/callback/".format(CALLBACK_URL), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}/callback/".format(CALLBACK_URL))

def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA
