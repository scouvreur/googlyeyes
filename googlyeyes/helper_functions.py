import numpy as np
import cv2
import requests

from uuid import UUID


def is_valid_uuid(uuid_to_test: str) -> bool:
    """
    Check if uuid_to_test is a valid v4 uuid.

    Parameters
    ----------
    uuid_to_test : str

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    >>> is_valid_uuid("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
    True
    >>> is_valid_uuid("c9bf9e58")
    False
    """
    try:
        UUID(uuid_to_test, version=4)
        return True
    except ValueError:
        return False


def buffer_to_image(input_bytes: bytes) -> np.ndarray:
    """
    Convert an input buffer into an image as a numpy array.

    Parameters
    ----------
    input_bytes: bytes
        Input bytes buffer.

    Returns
    -------
    output_image : np.ndarray
        Output image.
    """
    array = np.frombuffer(input_bytes, dtype='uint8')
    output_image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    return output_image


def POST_image(path, url) -> requests.models.Response:
    """
    Helper function to post an image as client.

    Parameters
    ----------
    path : str
        Path to image file to be posted.

    url : str
        API endpoint url to make the HTTP
        POST request.

    Returns
    -------
    response : requests.models.Response
        Response object from the server.
    """
    headers = {"content-type": "image/jpeg"}
    img = cv2.imread(path)
    # encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)
    # send http request with image and receive response
    response = requests.post(url, data=img_encoded.tostring(), headers=headers)
    return response
