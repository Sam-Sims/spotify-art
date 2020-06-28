from flask import Flask, render_template, redirect, session, request
import requests
from functions import functions

app = Flask(__name__)
config = functions.Config()
app.secret_key = config.secret_id
CLI_ID = config.client_id
CLI_SEC = config.secret_id
API_BASE = 'https://accounts.spotify.com'
SHOW_DIALOG = True
REDIRECT_URI = "http://127.0.0.1:5000/api_callback"

SCOPE = 'user-top-read'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/done')
def done():
    return render_template('done.html')

@app.route('/go', methods=['GET', 'POST'])
def go():
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    return redirect(auth_url)

@app.route('/go_analyse', methods=['GET','POST'])
def go_analyse():
    response = functions.get_user_top_artists(session['toke'])
    return render_template("results.html", data=response)

@app.route("/api_callback")
def api_callback():
    session.clear()
    code = request.args.get('code')

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:5000/api_callback",
        "client_id":CLI_ID,
        "client_secret":CLI_SEC
        })

    res_body = res.json()
    print(res.json())
    session["toke"] = res_body.get("access_token")

    return redirect("done")



if __name__ == '__main__':
    app.run()
