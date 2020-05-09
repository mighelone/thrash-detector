import os
from flask import Flask, render_template, request, redirect, url_for
import requests
import time
import glob

BASE_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(BASE_PATH, "static")
UPLOAD_FOLDER = "upload"

# remove uploaded files from previous sessions
for f in glob.iglob(os.path.join(STATIC_PATH, UPLOAD_FOLDER, "*.jpg")):
    os.remove(f)


app = Flask(__name__, static_folder=STATIC_PATH)

app.config.from_object(os.environ.get("FLASK_CONFIG", "frontend.config.TestConfig"))


content_type = "application/json"
headers = {"content-type": content_type}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        files = {
            "image1": request.files["image-1"].read(),
            "image2": request.files["image-2"].read(),
        }
        # import pdb; pdb.set_trace()
        try:
            response = requests.post("{}/api".format(app.config["BACKEND_URL"]), files=files)
        except requests.exceptions.ConnectionError:
            return render_template("index.html", error="Error accessing the backend")

        # import pdb; pdb.set_trace()
        first_jpg = f"first-{int(time.time())}.jpg"
        result_jpg = f"result-{int(time.time())}.jpg"
        with open(os.path.join(app.static_folder, UPLOAD_FOLDER, first_jpg), "wb") as f:
            f.write(files["image1"])
        if response.status_code == 200:
            with open(os.path.join(app.static_folder, UPLOAD_FOLDER, result_jpg), "wb") as f:
                f.write(response.content)
            error = None
        else:
            with open(os.path.join(app.static_folder, UPLOAD_FOLDER, result_jpg), "wb") as f:
                f.write(files["image2"])
            error = "Error detection bounding box"

        return render_template("index.html", filename=result_jpg, first=first_jpg, error=error)

    return render_template("index.html")


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename=os.path.join(UPLOAD_FOLDER, filename)), code=301)
