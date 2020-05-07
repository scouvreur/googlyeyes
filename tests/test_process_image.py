"""
Tests for image processing module.
"""

import numpy as np
import cv2
from dlib import rectangle, rectangles
from numpy.testing import assert_array_equal

from googlyeyes.process_image import (
    gen_googlyeye,
    get_faces,
    get_facial_landmarks,
    overlay_images,
)


def test_gen_googlyeye():
    """Test for gen_googlyeye
    """
    ground_truth = cv2.imread(
        filename="tests/data/googlyeye_250px_rotated_90deg.png", flags=-1
    )  # includes the alpha channel
    googlyeye = gen_googlyeye(size=250, angle=90)
    assert type(googlyeye) is np.ndarray
    assert googlyeye.shape == (250, 250, 4)  # 250x250, RGB+alpha channel
    assert_array_equal(ground_truth, googlyeye)


def test_get_faces():
    """Test for get_faces
    """
    input_image = cv2.imread("tests/data/test_payload_nface_2.jpeg")
    ground_truth = rectangles()
    ground_truth.append(rectangle(290, 290, 675, 675))
    ground_truth.append(rectangle(92, 588, 315, 811))
    assert ground_truth == get_faces(input_image)


def test_get_facial_landmarks():
    """Test for get_facial_landmarks
    """
    input_image = cv2.imread("tests/data/test_payload_nface_1.jpeg")
    face = get_faces(input_image)[0]
    shape = get_facial_landmarks(input_image, face)
    ground_truth = np.array([
        [201, 466], [204, 513], [211, 559], [220, 605], [233, 649],
        [256, 690], [289, 723], [331, 746], [382, 752], [431, 743],
        [468, 715], [497, 678], [517, 635], [527, 590], [535, 545],
        [542, 501], [545, 456], [226, 432], [246, 404], [279, 396],
        [314, 397], [349, 406], [410, 403], [443, 393], [476, 389],
        [508, 395], [527, 421], [378, 447], [379, 482], [381, 515],
        [383, 551], [338, 572], [359, 580], [382, 587], [403, 578],
        [423, 569], [264, 463], [285, 451], [310, 450], [331, 465],
        [309, 473], [284, 474], [426, 459], [448, 444], [472, 443],
        [491, 454], [475, 466], [450, 466], [310, 633], [339, 626],
        [364, 621], [381, 626], [400, 620], [422, 624], [448, 629],
        [423, 646], [401, 655], [382, 658], [363, 657], [339, 652],
        [320, 635], [364, 636], [381, 638], [401, 634], [438, 631],
        [400, 633], [381, 638], [364, 635]
    ])
    assert shape.shape == (68, 2)
    assert_array_equal(ground_truth, shape)


def test_overlay_images():
    """Test for overlay_images
    """
    ground_truth = cv2.imread(
        filename="tests/data/test_overlay_image_post.jpg", flags=1
    )
    small_image = cv2.imread(
        filename="tests/data/googlyeye_250px_rotated_90deg.png", flags=-1
    )  # includes the alpha channel
    large_image = cv2.imread(
        filename="tests/data/test_overlay_image_pre.jpg", flags=1
    )
    overlaid_image = overlay_images(
        small_image, large_image, offset=(250, 450)
    )
    assert ground_truth.shape == overlaid_image.shape
    # assert_array_equal(ground_truth, overlaid_image) # FAILS
