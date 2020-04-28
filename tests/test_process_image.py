from pathlib import Path
from PIL import Image, ImageChops

# from googlyeyes import process_image, rotate
from googlyeyes.rotate import rotate_eye


def test_visualize_facial_landmarks():
    # Test for visualize_facial_landmarks
    pass


def test_rotate_eye():
    # Test for rotate_eye
    base_path = Path(__file__).parent
    file_path = (base_path / "eye_rotated_90deg.png").resolve()
    ground_truth = Image.open(file_path)
    rotated_eye = rotate_eye(angle=90)

    def is_equal(im1, im2):
        # Determine if two images are equal pixel by pixel
        return ImageChops.difference(im1, im2).getbbox() is None

    assert is_equal(ground_truth, rotated_eye)
