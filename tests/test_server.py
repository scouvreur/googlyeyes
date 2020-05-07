"""
Test for web application REST API server module.
"""

import requests
import os

from googlyeyes.helper_functions import (
    is_valid_uuid,
    buffer_to_image,
    POST_image,
)
from googlyeyes.server import host, port

protocol = "http://"


def test_GET_imageUpload_endpoint():
    """Test for POST to /imageUpload endpoint
    """
    endpoint = "/imageUpload"
    url = protocol + host + ":" + str(port) + endpoint
    response = requests.get(url)
    assert response.ok
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_POST_imageUpload_endpoint():
    """Test for POST to /imageUpload endpoint
    """
    endpoint = "/imageUpload"
    url = protocol + host + ":" + str(port) + endpoint
    response = POST_image(path="tests/data/test_payload_nface_1.jpeg", url=url)
    output_image = buffer_to_image(response.content)
    filename = response.headers["Content-Disposition"].split('=')[1]
    uuid = filename.split('.')[0]
    assert response.ok
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"
    assert output_image.shape == (1024, 768, 3)
    assert response.elapsed.total_seconds() < 5
    assert is_valid_uuid(uuid)


def test_no_files_in_queue():
    """Test that after POST to /imageUpload endpoint, both input and output
    files are deleted from the queue folder
    """
    assert os.listdir("queue/") == []


def test_POST_test_endpoint():
    """Test for POST to /test endpoint
    """
    headers = {"content-type": "application/json"}
    payload = {"FirstName": "Stephane", "LastName": "Couvreur"}
    endpoint = "/test"
    url = protocol + host + ":" + str(port) + endpoint
    response = requests.post(url, json=payload, headers=headers)
    assert response.ok
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Request from Stephane Couvreur"


endpoint = "/imageUpload"
url = protocol + host + str(port) + endpoint