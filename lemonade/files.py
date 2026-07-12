import os

from . import crypto as c
from . import exceptions as e
from . import utils as u


LEMON_MAGIC = b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x92"
SOURKEY_MAGIC = b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x91"


def encrypt_to_file(
    data_bytes: bytes,
    lemonDirectory: str,
    sourkeyDirectory: str = ""
) -> None:
    """
    Encrypts binary data and stores it in Lemonade files.

    Creates two files:
        - A .lemon file containing encrypted data.
        - A .sourkey file containing the encryption key.

    Args:
        data (bytes):
            Binary data to encrypt.

        lemonDirectory (str):
            Directory where the .lemon file will be created.

        sourkeyDirectory (str, optional):
            Directory where the .sourkey file will be created.
            If empty, uses lemonDirectory.

    Raises:
        LemonadeError:
            When input types are invalid.

        InvalidPathError:
            When directories are invalid.
    """

    if not isinstance(data_bytes, bytes):
        raise e.LemonadeError(
            "Data must be bytes."
        )

    if not isinstance(lemonDirectory, str):
        raise e.LemonadeError(
            ".lemon directory path must be a string."
        )

    if not isinstance(sourkeyDirectory, str):
        raise e.LemonadeError(
            ".sourkey directory path must be a string."
        )

    if not os.path.isdir(lemonDirectory):
        raise e.InvalidPathError(
            ".lemon directory path must be a valid directory."
        )

    if sourkeyDirectory != "" and not os.path.isdir(sourkeyDirectory):
        raise e.InvalidPathError(
            ".sourkey directory path must be a valid directory."
        )

    if sourkeyDirectory == "":
        sourkeyDirectory = lemonDirectory

    lemon_path = u._get_available_filename(
        lemonDirectory,
        "lemonade.lemon"
    )

    sourkey_path = u._get_available_filename(
        sourkeyDirectory,
        "lemonade.sourkey"
    )

    crypt_bytes, key_bytes = c.encrypt(data_bytes)

    with open(lemon_path, "wb") as file:
        file.write(LEMON_MAGIC)
        file.write(crypt_bytes)

    with open(sourkey_path, "wb") as file:
        file.write(SOURKEY_MAGIC)
        file.write(key_bytes)


def decrypt_from_file(
    lemonFilePath: str,
    sourkeyFilePath: str
) -> bytes:
    """
    Decrypts data from Lemonade files.

    Reads a .lemon file and its corresponding .sourkey file,
    validates their headers, and restores the original data.

    Args:
        lemonFilePath (str):
            Path to the .lemon file.

        sourkeyFilePath (str):
            Path to the .sourkey file.

    Returns:
        bytes:
            Original decrypted data.

    Raises:
        InvalidLemonFileError:
            When the .lemon file header is invalid.

        InvalidSourkeyFileError:
            When the .sourkey file header is invalid.

        InvalidPathError:
            When file paths are invalid.
    """

    if not isinstance(lemonFilePath, str):
        raise e.LemonadeError(
            ".lemon file path must be a string."
        )

    if not isinstance(sourkeyFilePath, str):
        raise e.LemonadeError(
            ".sourkey file path must be a string."
        )

    if not os.path.isfile(lemonFilePath):
        raise e.InvalidPathError(
            ".lemon file path must be a valid file."
        )

    if not os.path.isfile(sourkeyFilePath):
        raise e.InvalidPathError(
            ".sourkey file path must be a valid file."
        )

    with open(lemonFilePath, "rb") as file:
        magic = file.read(len(LEMON_MAGIC))

        if magic != LEMON_MAGIC:
            raise e.InvalidLemonFileError(
                "Invalid .lemon file."
            )

        crypt_bytes = file.read()

    with open(sourkeyFilePath, "rb") as file:
        magic = file.read(len(SOURKEY_MAGIC))

        if magic != SOURKEY_MAGIC:
            raise e.InvalidSourkeyFileError(
                "Invalid .sourkey file."
            )

        key_bytes = file.read()

    return c.decrypt(crypt_bytes, key_bytes)