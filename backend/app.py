from io import BytesIO

from flask import Flask, request, jsonify, send_file, abort

from recycleye.detect import trash_detect

def read_image(img: str) -> bytes:
    with open(img, "rb") as image:
        return image.read()


app = Flask(__name__)

@app.route("/api", methods=["POST"])
def detect_thrash():
    try:
        img1 = request.files["image1"].read()
    except KeyError:
        abort(404)
    try:
        img2 = request.files["image2"].read()
    except KeyError:
        abort(404)
    try:
        res = trash_detect(image1=img1, image2=img2, min_area=500)
    except:
        abort(400)
    # TODO check how to pass also the bounding box
    return send_file(
        BytesIO(res.processed_image), mimetype='image/jpeg'
    )