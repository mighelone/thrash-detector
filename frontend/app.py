import os
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

app.config.from_object(os.environ.get(
    "FLASK_CONFIG", "frontend.config.TestConfig"
))


content_type = "application/json"
headers = {'content-type': content_type}

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def hello():
    print(request)
    if request.method == "POST":
        if request.files:

            img1 = request.files["image-1"]
            img2 = request.files["image-2"]
            files = {
                "image1": request.files["image-1"],
                "image2": request.files["image-2"],
            }
            response = requests.post("{}/post".format(app.config["BACKEND_URL"]), files=files)
            return render_template("index.html", comment="Done!")

    return render_template("index.html")