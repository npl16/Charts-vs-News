#Adapated from Flask-Spotify-Auth code by Greg Van Ort available at https://github.com/vanortg/Flask-Spotify-Auth

import base64, json, requests

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''

def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, scope)
    return data

def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
#Modified to work with Python3.6 and up:
    res = "{}:{}".format(client_id, client_secret)
    bres = res.encode("UTF-8")
    encoded = base64.b64encode(bres)
    decoded = encoded.decode('ascii')
    #encoded = base64.b64encode("{}:{}".format(client_id, client_secret))
            #See: https://www.pronoy.in/2016/10/20/python-3-5-x-base64-encoding-3/
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(decoded)}

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    return handleToken(json.loads(post.text))

def handleToken(response):
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

def refreshAuth():
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : REFRESH_TOKEN
    }

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=HEADER)
    p_back = json.dumps(post_refresh.text)

    return handleToken(p_back)
