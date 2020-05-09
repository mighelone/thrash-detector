import os
from flask import Flask, render_template, request, redirect, url_for
import requests

BASE_PATH = os.path.dirname(__file__)
app = Flask(__name__, static_folder=os.path.join(BASE_PATH, "static"))

app.config.from_object(os.environ.get("FLASK_CONFIG", "frontend.config.TestConfig"))


content_type = "application/json"
headers = {"content-type": content_type}


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files:

            files = {
                "image1": request.files["image-1"].read(),
                "image2": request.files["image-2"].read(),
            }
            response = requests.post("{}/api".format(app.config["BACKEND_URL"]), files=files)
            with open(os.path.join(app.static_folder, "upload/result.jpg"), "wb") as f:
                f.write(response.content)
            return render_template("index.html", filename="result.jpg")

    return render_template("index.html")


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename=os.path.join("upload/", filename)), code=301)
