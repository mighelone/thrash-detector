import json
import cv2
import numpy as np
import requests
import sys
import click
import base64
from io import BufferedReader, BufferedWriter


# res = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)


@click.command()
@click.argument(
    "image1", type=click.File(mode="rb"), required=True,
)
@click.argument(
    "image2", type=click.File(mode="rb"), required=True,
)
@click.option(
    "--url",
    "-u",
    type=click.STRING,
    default="http://localhost:8000",
    help="URL of the API server",
    show_default=True,
)
@click.option(
    "--output",
    "-o",
    type=click.File(mode="wb"),
    default="result.jpg",
    help="Output path of the resulting file",
    show_default=True,
)
@click.option("--verbose/--no-verbose", "-v", default=False, help="Verbose mode")
@click.option("--display/--no-display", "-d", default=True, help="Display image")
def main(
    image1: BufferedReader,
    image2: BufferedReader,
    url: str,
    output: BufferedWriter,
    verbose: bool,
    display: bool,
):
    """
    Thrash detector API client. 
    """
    files = {"image1": image1.read(), "image2": image2.read()}
    url_path = url.rstrip("/") + "/api/thrash/json"
    if verbose:
        click.echo(f"Querying thrash detector API on {url_path}")
        click.echo(f"Image 1: {image1.name}")
        click.echo(f"Image 2: {image2.name}")

    response = requests.post(url_path, files=files)

    if response.status_code != 200:
        click.echo(message=f"API request failed with code {response.status_code}.", err=True)
        click.echo(message=f"{response.json()['error']}", err=True)
        sys.exit(response.status_code)

    data = response.json()
    image = data["encoded_img"]["bytes"]
    bounds = data["bounds"]
    if verbose:
        click.echo(f"Bounding box: {bounds}")
        click.echo(f"Save bounding box image to {output.name}")

    image = base64.decodebytes(image.encode("ascii"))
    output.write(image)

    if display:
        res = cv2.imdecode(np.frombuffer(image, np.uint8), -1)
        cv2.imshow("bounding box", res)
        click.echo("Press any key to close the image")
        cv2.waitKey(0)


if __name__ == "__main__":
    main()
