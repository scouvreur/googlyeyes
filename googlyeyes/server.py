#!/usr/bin/python3
from flask import Flask, request
from flask_restful import Resource, Api

# from process_image import visualize_facial_landmarks

app = Flask(__name__)
api = Api(app)


class ImageUpload(Resource):
    def get(self):
        return {"status": "success"}

    def post(self):
        return {"status": "success"}


class Test(Resource):
    def post(self):
        LastName = request.json["LastName"]
        FirstName = request.json["FirstName"]
        result = {
            "status": "success",
            "message": "Request from {} {}".format(FirstName, LastName),
        }
        return result


# Add image POST endpoint
api.add_resource(ImageUpload, "/imageUpload")
api.add_resource(Test, "/test")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
