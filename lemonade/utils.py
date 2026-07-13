import os
import hashlib


def _calculate_sha256(data: bytes) -> str:
    """
    Calculates the SHA-256 hash of binary data.

    Args:
        data (bytes):
            Data to hash.

    Returns:
        str:
            SHA-256 hash in hexadecimal.
    """

    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes.")

    return hashlib.sha256(data).hexdigest()


def _verify_sha256(data: bytes, expected_hash: str) -> bool:
    """
    Verifies the SHA-256 hash of binary data.
    """

    return _calculate_sha256(data) == expected_hash


def _get_available_filename(directory: str, filename: str) -> str:
    """
    Generates an available file path by adding a numeric suffix.

    The function starts checking from the first suffix and increments
    the number until it finds a filename that does not already exist.

    Example:
        "lemonade.lemon" becomes:

        lemonade_1.lemon
        lemonade_2.lemon
        lemonade_3.lemon

    Args:
        directory (str):
            Directory where the file will be created.

        filename (str):
            Base filename, including extension.

    Returns:
        str:
            Available file path.
    """
    
    name, extension = os.path.splitext(filename)

    n = 1

    new_filename = f"{name}_{n}{extension}"
    path = os.path.join(directory, new_filename)

    while os.path.exists(path):
        n += 1
        new_filename = f"{name}_{n}{extension}"
        path = os.path.join(directory, new_filename)

    return path