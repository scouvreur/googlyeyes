"""
Test for web application REST API server module.
"""

import requests
import numpy as np

from googlyeyes.helper_functions import (
    is_valid_uuid,
    buffer_to_image,
    POST_image,
)
from googlyeyes.server import host, port

scheme = "http://"


def test_GET_imageUpload_endpoint():
    """Test for POST to /imageUpload endpoint
    """
    endpoint = "/imageUpload"
    url = scheme + host + ":" + str(port) + endpoint
    response = requests.get(url)
    assert response.ok
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_POST_imageUpload_endpoint():
    """Test for POST to /imageUpload endpoint
    """
    endpoint = "/imageUpload"
    url = scheme + host + ":" + str(port) + endpoint
    response = POST_image(path="tests/data/test_payload_nface_1.jpeg", url=url)
    output_image = buffer_to_image(response.content)
    filename = response.headers["Content-Disposition"].split('=')[1]
    uuid = filename.split('.')[0]
    assert response.ok
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"
    assert output_image.shape == (1024, 768, 3)
    assert is_valid_uuid(uuid)
    return response.elapsed.total_seconds()


def test_server_performance_syncronous():
    """Test for POST to /imageUpload endpoint
    """
    response_times = []
    for _ in range(100):
        response_times.append(test_POST_imageUpload_endpoint())
    response_times_array_ms = np.array(response_times, dtype=np.float64)*1000
    mean_response_time_ms = np.mean(response_times_array_ms)
    three_9s_response_time_ms = np.percentile(response_times_array_ms, 99.9)
    five_9s_response_time_ms = np.percentile(response_times_array_ms, 99.999)
    assert mean_response_time_ms < 500.0
    assert three_9s_response_time_ms < 750.0
    assert five_9s_response_time_ms < 1000.0
    return {
        "mean_response_time_ms": mean_response_time_ms,
        "three_9s_response_time_ms": three_9s_response_time_ms,
        "five_9s_response_time_ms": five_9s_response_time_ms,
    }


def test_POST_test_endpoint():
    """Test for POST to /test endpoint
    """
    headers = {"content-type": "application/json"}
    payload = {"FirstName": "Stephane", "LastName": "Couvreur"}
    endpoint = "/test"
    url = scheme + host + ":" + str(port) + endpoint
    response = requests.post(url, json=payload, headers=headers)
    assert response.ok
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Request from Stephane Couvreur"
