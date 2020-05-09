"""
detect module
=============
Contains:
    `TrashDetectorResult`
    `trash_detect`

"""
from typing import Tuple, Optional

import attr
import cv2
import imutils
import numpy as np


MIN_AREA = 500

BLUR_KSIZE = (21, 21)


@attr.s
class TrashDetectorResult:
    bounds: Tuple[int, int, int, int] = attr.ib()
    processed_image: bytes = attr.ib()
    source_image_1: bytes = attr.ib()
    source_image_2: bytes = attr.ib()


def trash_detect(
    image1: bytes, image2: bytes, min_area=MIN_AREA
) -> TrashDetectorResult:

    image1_cv = _image_from_bytes(image1)
    image2_cv = _image_from_bytes(image2)

    image1_grey = _convert_image_to_greyscale_and_blur(image1_cv, ksize=BLUR_KSIZE)
    image2_grey = _convert_image_to_greyscale_and_blur(image2_cv, ksize=BLUR_KSIZE)

    image_result = image2_cv.copy()

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(image1_grey, image2_grey)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image_result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, encoded = cv2.imencode(".jpg", image_result, encode_param)
    return TrashDetectorResult(
        bounds=(x, y, w, h),
        processed_image=bytes(encoded),
        source_image_1=image1,
        source_image_2=image2,
    )


def _image_from_bytes(image: bytes) -> np.ndarray:
    """Convert image in buytes into a nmumpy array

    Arguments:
        image {bytes} -- Image in bytes

    Returns:
        np.ndarray -- Converted image in numpy array
    """
    img = cv2.imdecode(np.frombuffer(image, np.uint8), -1)
    return imutils.resize(img, width=500)


def _convert_image_to_greyscale_and_blur(
    image: np.ndarray, ksize: Optional[Tuple[int, int]] = None
) -> np.ndarray:
    """Convert an image array into greyscale and optionally blur the image

    Arguments:
        image {np.ndarray} -- Original image with color

    Keyword Arguments:
        ksize {Optional[Tuple[int, int]]} -- Ksize for blur the image. 
            If None no blur is applied (default: {None})

    Returns:
        np.ndarray -- Converted image
    """
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if ksize:
        image_grey = cv2.GaussianBlur(image_grey, (21, 21), 0)
    return image_grey


def read_image(img):
    with open(img, "rb") as image:
        return image.read()
