"""
Web application REST API server module.
"""

import uuid
import logging

from flask import Flask, Response, request
from flask_restful import Resource, Api
from werkzeug.datastructures import Headers

from googlyeyes.process_image import process
from googlyeyes.helper_functions import buffer_to_image, image_to_buffer

app = Flask(__name__)
api = Api(app)


class ImageUpload(Resource):
    def get(self):
        response = {"status": "success"}
        return response

    def post(self):
        # Decode image
        input_image = buffer_to_image(request.data)
        output_uuid = str(uuid.uuid4())
        # Process image
        output_image = process(input_image)
        # Create response headers
        header = Headers()
        header.add("Content-Type", "image/jpeg")
        header.add(
            "Content-Disposition",
            "attachment",
            filename=output_uuid + ".jpg"
        )
        return Response(
            response=image_to_buffer(output_image),
            status=200,
            headers=header
        )


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
