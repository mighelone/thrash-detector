from io import BytesIO

from flask import Flask, request, jsonify, send_file, abort, make_response

from recycleye.detect import trash_detect


def read_image(img: str) -> bytes:
    with open(img, "rb") as image:
        return image.read()


app = Flask(__name__)


@app.errorhandler(400)
def error_detection(e):
    return jsonify(error=str(e)), 400


@app.route("/api", methods=["POST"])
def detect_thrash():
    try:
        img1 = request.files["image1"].read()
    except KeyError:
        abort(400, description="File image1 not defined!")
    try:
        img2 = request.files["image2"].read()
    except KeyError:
        abort(400, description="File image2 not defined!")
    try:
        res = trash_detect(image1=img1, image2=img2, min_area=500)
    except Exception as e:
        abort(400, description=f"Error during thrash detection: {e}")
    # TODO check how to pass also the bounding box
    response = send_file(BytesIO(res.processed_image), mimetype="image/jpeg")
    return response
