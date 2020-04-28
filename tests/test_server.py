import requests

# import cv2

# TO-DO read this from server.py
host = "http://127.0.0.1:5000"


def test_GET_imageUpload_endpoint():
    # Test for POST to /imageUpload endpoint
    url = host + "/imageUpload"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_POST_imageUpload_endpoint():
    # Test for POST to /imageUpload endpoint
    headers = {"content-type": "image/jpeg"}
    image = open("tests/test_payload.jpeg", "rb").read()
    url = host + "/imageUpload"
    response = requests.post(url, data=image, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


# def test_POST_imageUpload_endpoint():
#     # Test for POST to /imageUpload endpoint
#     headers = {"content-type": "image/jpeg"}
#     image = cv2.imread("tests/test_payload.jpeg")
#     _, image_encoded = cv2.imencode('.jpg', image)
#     url = host + "/imageUpload"
    # response = requests.post(url,
    #                          data=image_encoded.tostring(),
    #                          headers=headers)
#     # assert response.status_code == 200
#     pass


def test_POST_test_endpoint():
    # Test for POST to /test endpoint
    headers = {"content-type": "application/json"}
    payload = {"FirstName": "Stephane", "LastName": "Couvreur"}
    url = host + "/test"
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Request from Stephane Couvreur"
