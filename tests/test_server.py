"""
Test for web application REST API server module.
"""

import requests
import cv2
import os

from tests.helpers import is_valid_uuid

# TO-DO read this from server.py
host = "http://0.0.0.0:5000"


def POST_image(path, url):
    """Helper function to post an image
    """
    headers = {"content-type": "image/jpeg"}
    img = cv2.imread(path)
    # encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)
    # send http request with image and receive response
    response = requests.post(url, data=img_encoded.tostring(), headers=headers)
    return response


def test_GET_imageUpload_endpoint():
    """Test for POST to /imageUpload endpoint
    """
    url = host + "/imageUpload"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_POST_imageUpload_endpoint():
    """Test for POST to /imageUpload endpoint
    """
    url = host + "/imageUpload"
    response = POST_image(path="tests/test_payload_nface_1.jpeg", url=url)
    assert response.status_code == 200
    # assert response.json()["status"] == "success"
    # assert response.json()["message"] == "Image received. Size=768x1024"
    # assert is_valid_uuid(response.json()["uuid"])


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
    url = host + "/test"
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Request from Stephane Couvreur"
