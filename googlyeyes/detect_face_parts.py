"""
Eye detection module.
"""

from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import random

from googlyeyes.rotate import rotate_eye


description = """
Command line tool to detect face parts.
"""

# construct the argument parser and parse the arguments
parser = argparse.ArgumentParser(
    prog="detect_face_parts", description=description
)
parser.add_argument(
    "-p",
    "--shape-predictor",
    required=False,
    default="resources/shape_predictor_68_face_landmarks.dat",
    help="path to facial landmark predictor",
)
parser.add_argument(
    "-i",
    "--image",
    required=False,
    default="tests/test_payload.jpeg",
    help="path to input image",
)
args = vars(parser.parse_args())


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# load the input image, resize it, and convert it to grayscale
image = cv2.imread(args["image"])
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
faces = detector(gray, 1)

facial_landmark_coords = {
    "right_eye": (36, 42),
    "left_eye": (42, 48),
}

googlyeye = rotate_eye(angle=random.randint(0, 360))
# googlyeye_array = np.asarray(googlyeye)

googlyeye = cv2.imread("resources/eye2.png", -1)
googlyeye = cv2.resize(googlyeye, (50, 50))

# loop over all faces detected in image
for (i, face) in enumerate(faces):
    # determine the facial landmarks for the face region, then
    # convert the landmark (x, y)-coordinates to a NumPy array
    shape = predictor(gray, face)
    shape = face_utils.shape_to_np(shape)

    # loop over the face parts individually
    for (landmark, (i, j)) in facial_landmark_coords.items():
        # clone the original image so we can draw on it, then
        # display the landmark of the face part on the image
        clone = image.copy()
        cv2.putText(
            clone,
            landmark,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        # loop over the subset of facial landmarks, drawing the
        # specific face part
        for (x, y) in shape[i:j]:
            cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)

        # extract the ROI of the face region as a separate image
        (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
        roi = image[y:y+h, x:x+w]
        roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)

        s_img = googlyeye

        facial_landmark_coords[landmark]
        if landmark == "right_eye":
            index = 37
        elif landmark == "left_eye":
            index = 43
        else:
            pass

        x_offset, y_offset = tuple(shape[index])

        y1, y2 = y_offset, y_offset + s_img.shape[0]
        x1, x2 = x_offset, x_offset + s_img.shape[1]

        alpha_s = s_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            clone[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                      alpha_l * clone[y1:y2, x1:x2, c])

        # show the particular face part
        cv2.imshow("ROI", roi)
        cv2.imshow("Image", clone)
        cv2.waitKey(0)
