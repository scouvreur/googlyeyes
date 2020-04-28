from PIL import Image
from pathlib import Path


def rotate_eye(angle):
    """
    Returns rotated googly eye.

    Parameters
    ----------
    angle : int
        Angle to rotate from reference.
        Can be between 0 and 360 degrees.

    Returns
    -------
    rotated_eye : PIL image object
        Image rotated by angle.
    """
    base_path = Path(__file__).parent
    file_path = (base_path / "../resources/eye.png").resolve()
    eye = Image.open(file_path)
    rotated_eye = eye.rotate(angle)
    return rotated_eye
