"""
Web application REST API server module.
"""

import cv2
import uuid
import os
import logging

from flask import Flask, request, send_file
from flask_restful import Resource, Api

from googlyeyes.process_image import process
from googlyeyes.helper_functions import buffer_to_image

app = Flask(__name__)
api = Api(app)


class ImageUpload(Resource):
    def get(self):
        response = {"status": "success"}
        return response

    def post(self):
        try:
            os.mkdir("queue/")
        except FileExistsError:
            pass
        # decode image
        input_image = buffer_to_image(request.data)
        input_uuid, output_uuid = str(uuid.uuid4()), str(uuid.uuid4())
        cv2.imwrite("queue/" + input_uuid + ".jpg", input_image)
        # Process image
        output_image = process(input_image)
        # Write processed image to disk and send it back in response
        cv2.imwrite("queue/" + output_uuid + ".jpg", output_image)
        try:
            return send_file("../queue/" + output_uuid + ".jpg",
                             as_attachment=True)
        finally:
            os.remove("queue/" + input_uuid + ".jpg")
            os.remove("queue/" + output_uuid + ".jpg")


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

host = "0.0.0.0"
port = 5000

if __name__ == "__main__":
    logging.basicConfig(filename="server.log", level=logging.DEBUG)
    app.run(host=host, port=port, debug=True)
