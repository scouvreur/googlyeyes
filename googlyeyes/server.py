"""
Web application REST API server module.
"""

import numpy as np
import cv2
import uuid
import os
import logging

from flask import Flask, request
from flask_restful import Resource, Api

from process_image import process

app = Flask(__name__)
api = Api(app)


class ImageUpload(Resource):
    def get(self):
        response = {"status": "success"}
        return response

    def post(self):
        # convert string of image data to uint8
        array = np.fromstring(request.data, np.uint8)
        # decode image
        input_image = cv2.imdecode(array, cv2.IMREAD_COLOR)
        input_uuid, output_uuid = str(uuid.uuid4()), str(uuid.uuid4())
        cv2.imwrite("queue/" + input_uuid + ".jpg", input_image)
        # Process image
        output_image = process(input_image)
        cv2.imwrite("queue/" + output_uuid + ".jpg", output_image)
        # Write processed image to disk and send it back in response
        os.remove("queue/" + input_uuid + ".jpg")
        os.remove("queue/" + output_uuid + ".jpg")
        response = {
            "status": "success",
            "message": "Image received. Size={}x{}".format(
                input_image.shape[1], input_image.shape[0]
            ),
            "uuid": input_uuid,
        }
        return response


class Test(Resource):
    def post(self):
        LastName = request.json["LastName"]
        FirstName = request.json["FirstName"]
        response = {
            "status": "success",
            "message": "Request from {} {}".format(FirstName, LastName),
        }
        return response


# Add image POST endpoint
api.add_resource(ImageUpload, "/imageUpload")
api.add_resource(Test, "/test")


if __name__ == "__main__":
    logging.basicConfig(filename="server.log", level=logging.DEBUG)
    app.run(host="127.0.0.1", port=5000, debug=True)
