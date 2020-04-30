from uuid import UUID


def is_valid_uuid(uuid_to_test: str) -> bool:
    """
    Check if uuid_to_test is a valid v4 uuid.

    Parameters
    ----------
    uuid_to_test : str

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    >>> is_valid_uuid("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
    True
    >>> is_valid_uuid("c9bf9e58")
    False
    """
    try:
        UUID(uuid_to_test, version=4)
        return True
    except ValueError:
        return False
