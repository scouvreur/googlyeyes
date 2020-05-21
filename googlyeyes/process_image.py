"""
Image processing module.
"""

from imutils import face_utils, rotate_bound
import numpy as np
import dlib
import cv2
import random

# Instantiate detectors only once
# Initialize facial landmark predictor
predictor = dlib.shape_predictor(
    "resources/shape_predictor_68_face_landmarks.dat"
)

# Initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector()


def gen_googlyeye(size: int, angle: int) -> np.ndarray:
    """
    Helper function to generate a googlyeye.

    Parameters
    ----------
    size : int
        Size of the googlyeye image in pixels in both
        x and y dimentions (the image is square).

    angle : int
        Angle to rotate the image by in degrees. Can be
        between 0 and 360.

    Returns
    -------
    googlyeye : np.ndarray
        Image of the googlyeye as a numpy array.
    """
    googlyeye = cv2.imread(
        filename="resources/googlyeye.png", flags=-1
    )  # includes the alpha channel
    googlyeye = cv2.resize(googlyeye, (size, size))
    googlyeye = rotate_bound(googlyeye, angle)
    return googlyeye


def get_faces(input_image: np.ndarray) -> dlib.rectangles:
    """
    Helper function to get the list of face bounding boxes.

    Parameters
    ----------
    input_image : np.ndarray
        Image to be processed.

    Returns
    -------
    faces : dlib.rectangles
        List of arrays of face bounding boxes coordinates.
    """
    # load input image, resize it, and convert it to grayscale
    # input_image = imutils.resize(input_image, width=500)
    grayscale = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscalescale image
    faces = detector(grayscale, 1)
    return faces


def get_facial_landmarks(
    input_image: np.ndarray, face: dlib.rectangle
) -> np.ndarray:
    """
    Helper function to get the array of 68 facial landmarks.

    Parameters
    ----------
    input_image : np.ndarray
        Image to be processed.

    face : dlib.rectangle
        Array of face bounding boxes coordinates.

    Returns
    -------
    shape : np.ndarray
        Array of [x, y] coordinates in pixels of the 68
        facial landmarks.
    """
    grayscale = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    shape = predictor(grayscale, face)
    shape = face_utils.shape_to_np(shape)
    return shape


def overlay_images(
    small_image: np.ndarray, large_image: np.ndarray, offset: (int, int)
) -> np.ndarray:
    """
    Overlay a smaller image with an alpha channel onto a
    larger one.

    Parameters
    ----------
    small_image, large_image : np.ndarray
        Small and large images to be overlaid. The
        small image should have an alpha channel.

    offset : Tuple(int, int), (x_offset, y_offset)
        Offset in pixels of the small image from the top
        left corner of the large image.

    Returns
    -------
    output_image : np.ndarray
        Output image with the overlay as a numpy array.
    """
    output_image = large_image.copy()
    channels = 3
    x_offset, y_offset = offset
    y1, y2 = y_offset, y_offset + small_image.shape[0]
    x1, x2 = x_offset, x_offset + small_image.shape[1]
    alpha_s = small_image[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    for channel in range(channels):
        output_image[y1:y2, x1:x2, channel] = (
            alpha_s * small_image[:, :, channel]
            + alpha_l * large_image[y1:y2, x1:x2, channel]
        )
    return output_image


def process(input_image: np.ndarray) -> np.ndarray:
    """
    Process input image from start to finish.

    Parameters
    ----------
    input_image : np.ndarray
        Image to be processed.

    Returns
    -------
    output_image : np.ndarray
        Output image with the googlyeyes on each face
        as a numpy array.
    """
    facial_landmark_coords = {
        "right_eye": (36, 42),
        "left_eye": (42, 48),
    }

    faces = get_faces(input_image)

    copy = input_image.copy()
    # loop over all faces detected in image
    for (i, face) in enumerate(faces):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = get_facial_landmarks(input_image, face)

        # loop over the face parts individually
        for (landmark, (i, j)) in facial_landmark_coords.items():
            small_image = gen_googlyeye(
                size=random.randint(25, 50), angle=random.randint(0, 360)
            )
            if landmark == "right_eye":
                index = 37
            elif landmark == "left_eye":
                index = 43

            copy = overlay_images(
                small_image=small_image,
                large_image=copy,
                offset=tuple(shape[index]),
            )
    return copy


def save_lossles_jpeg(path: str, image: np.ndarray) -> None:
    cv2.imwrite(
        path,
        image,
        [
            int(cv2.IMWRITE_JPEG_QUALITY), 100,
            int(cv2.IMWRITE_JPEG_PROGRESSIVE), 1,
            int(cv2.IMWRITE_JPEG_OPTIMIZE), 1,
            int(cv2.IMWRITE_JPEG_RST_INTERVAL), 65535,
            int(cv2.IMWRITE_JPEG_LUMA_QUALITY), 100,
            int(cv2.IMWRITE_JPEG_CHROMA_QUALITY), 100,
        ],
    )
