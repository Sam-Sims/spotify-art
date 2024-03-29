from flask import Flask, render_template, redirect, session, request, send_file, send_from_directory
import requests
from functions import functions
from functions import imaging
from os import environ

app = Flask(__name__)
# config = functions.Config()
# CLI_ID = config.client_id
# CLI_SEC = config.secret_id
app.secret_key = environ.get("secret")
CLI_ID = environ.get("client")
CLI_SEC = environ.get("secret")
deploy_type = environ.get("deploy_type")
if deploy_type == "local":
    REDIRECT_URI = "http://127.0.0.1:5000/api_callback"
elif deploy_type == "render":
    REDIRECT_URI = "https://spotify-flask.onrender.com/api_callback"
else:
    REDIRECT_URI = "https://spotify-flask.onrender.com/api_callback"

API_BASE = "https://accounts.spotify.com"
SHOW_DIALOG = True
SCOPE = "user-top-read"


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/hub")
def hub():
    return render_template("hub.html")


@app.route("/go", methods=["GET", "POST"])
def go():
    auth_url = f"{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}"
    return redirect(auth_url)


@app.route("/go_top_artist", methods=["POST"])
def go_analyse_artist():
    if request.form["submit_artist"] == "Top Lockdown artists":
        response = functions.get_user_top_artists(session["toke"], "short_term")
    elif request.form["submit_artist"] == "Top Artists (6 months)":
        response = functions.get_user_top_artists(session["toke"], "medium_term")
    elif request.form["submit_artist"] == "Top Artists (All time)":
        response = functions.get_user_top_artists(session["toke"], "long_term")
    return render_template("results.html", data=response)


@app.route("/go_top_track", methods=["POST"])
def go_analyse_track():
    if request.form["submit_tracks"] == "Top Lockdown tracks":
        response = functions.get_user_top_tracks(session["toke"], "short_term")
    elif request.form["submit_tracks"] == "Top Tracks (6 months)":
        response = functions.get_user_top_tracks(session["toke"], "medium_term")
    elif request.form["submit_tracks"] == "Top Tracks (All time)":
        response = functions.get_user_top_tracks(session["toke"], "long_term")
    return render_template("results.html", data=response)


@app.route("/get_image", methods=["GET"])
def send_image():
    response = functions.get_visulisation_values(session["toke"])
    averages = functions.average_features(response)
    img = imaging.construct_image(functions.evaluate(averages))
    served_image = functions.serve_img(img)
    return send_file(served_image, mimetype="image/PNG")


@app.route("/go_top_visualise", methods=["POST"])
def go_visualise():
    response = functions.get_visulisation_values(session["toke"])
    evaluation = functions.evaluate(functions.average_features(response))
    report = functions.construct_report(evaluation)
    return render_template("visulise.html", report=report)


@app.route("/go_top_visualise_js", methods=["GET", "POST"])
def go_visualise_js():
    response = functions.get_visulisation_values(session["toke"])
    data = functions.average_features(response)
    report = functions.construct_report_js(data)
    print(data)
    return render_template("p5js.html", data=data, report=report)


@app.route("/api_callback")
def api_callback():
    session.clear()
    code = request.args.get("code")

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(
        auth_token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLI_ID,
            "client_secret": CLI_SEC,
        },
    )

    res_body = res.json()
    session["toke"] = res_body.get("access_token")

    return redirect("go_top_visualise_js")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run()
