import os
import hashlib

from .metadata_type import MetadataType
from .metadata import MetadataField


def _calculate_sha256(data: bytes) -> bytes:
    """
    Calculates the SHA-256 hash of binary data.

    Args:
        data (bytes):
            Data to hash.

    Returns:
        bytes:
            SHA-256 hash in raw binary format.
    """

    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes.")

    return hashlib.sha256(data).digest()


def _verify_sha256(
    data: bytes,
    expected_hash: bytes
) -> bool:
    """
    Verifies the SHA-256 hash of binary data.
    """

    return _calculate_sha256(data) == expected_hash



def _get_metadata_field(
    fields: list[MetadataField],
    identifier: MetadataType
) -> bytes | None:
    for field in fields:
        if field.identifier == identifier:
            return field.data

    return None


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