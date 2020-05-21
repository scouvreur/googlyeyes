"""
Tests for image processing module.
"""

import pytest
import cv2
import numpy as np
from numpy.testing import assert_array_equal

from googlyeyes.server import host, port
from googlyeyes.helper_functions import (
    is_valid_uuid,
    buffer_to_image,
    POST_image,
)

scheme = "http://"


def test_is_valid_uuid():
    """Test for is_valid_uuid function
    """
    assert is_valid_uuid("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
    assert not is_valid_uuid("c9bf9e58")
    assert not is_valid_uuid("")
    with pytest.raises(TypeError):
        is_valid_uuid(None)
    with pytest.raises(AttributeError):
        is_valid_uuid(0)


def test_buffer_to_image():
    """Test for buffer_to_image function
    """
    img = cv2.imread("tests/data/test_buffer.jpg")
    # encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)
    img_bytes = img_encoded.tostring()
    ground_truth = np.array(
        [[[1, 1, 1], [254, 254, 254]], [[252, 252, 252], [255, 255, 255]]],
        dtype=np.uint8,
    )
    output = buffer_to_image(input_bytes=img_bytes)
    assert_array_equal(output, ground_truth)
    assert ground_truth.shape == output.shape


def test_POST_image():
    """Test for POST_image function
    """
    path = "tests/data/test_buffer.jpg"
    endpoint = "/imageUpload"
    url = scheme + host + ":" + str(port) + endpoint
    response = POST_image(path, url)
    assert response.ok
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"
    assert response.headers["Content-Length"] == "682"
