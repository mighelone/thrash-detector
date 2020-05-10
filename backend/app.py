from io import BytesIO

from flask import Flask, request, jsonify, send_file, abort, make_response

from recycleye.detect import trash_detect
import base64

ENCODING = "ascii"

app = Flask(__name__)


@app.errorhandler(400)
def error_detection(e):
    return jsonify(error=str(e)), 400


@app.route("/api/thrash/image", methods=["POST"])
def detect_thrash_image():
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
    return send_file(BytesIO(res.processed_image), mimetype="image/jpeg")


@app.route("/api/thrash/json", methods=["POST"])
def detect_thrash_json():
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

    encoded_img = base64.encodebytes(res.processed_image).decode(ENCODING)

    payload = {"bounds": res.bounds, "encoded_img": {"bytes": encoded_img, "encoding": ENCODING,}}
    # TODO check how to pass also the bounding box
    # response = send_file(BytesIO(res.processed_image), mimetype="image/jpeg")
    return jsonify(payload)
