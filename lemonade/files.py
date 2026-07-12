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
        
        
def encrypt_with_sourkey_to_file(
    data_bytes: bytes,
    lemonDirectory: str,
    sourkeyFilePath: str
) -> None:
    """
    Encrypts binary data using an existing .sourkey file and creates a .lemon file.

    This function reads an existing Lemonade sourkey file, extracts the stored
    encryption key, encrypts the provided data using that key, and saves the
    encrypted result as a .lemon file.

    The encryption process uses the key stored in the .sourkey file:

        C = (M - K) mod 256

    Where:
        C = encrypted byte
        M = original data byte
        K = key byte

    If the key is shorter than the input data, the key bytes are repeated
    cyclically during encryption.

    The generated .lemon file contains:

        LEMON_MAGIC + encrypted data

    Args:
        data_bytes (bytes):
            Binary data to be encrypted.

        lemonDirectory (str):
            Directory where the generated .lemon file will be saved.

        sourkeyFilePath (str):
            Path to the existing .sourkey file containing the encryption key.

    Returns:
        None

    Raises:
        LemonadeError:
            When the input data or paths are invalid.

        InvalidPathError:
            When the provided directory or file path does not exist or
            has an invalid type.

        InvalidSourkeyFileError:
            When the provided .sourkey file does not contain a valid
            Lemonade sourkey header.
    """
    
    if not isinstance(data_bytes, bytes):
        raise e.LemonadeError(
            "Data must be bytes."
        )
        
    if not isinstance(lemonDirectory, str):
        raise e.LemonadeError(
            ".lemon directory path must be a string."
        )
        
    if not isinstance(sourkeyFilePath, str):
        raise e.LemonadeError(
            ".sourkey file path must be a string."
        )
        
    if not os.path.isdir(lemonDirectory):
        raise e.InvalidPathError(
            ".lemon directory path must be a valid directory."
        )
        
    if not os.path.isfile(sourkeyFilePath):
        raise e.InvalidPathError(
            ".sourkey file path must be a valid file."
        )
        
    lemon_path = u._get_available_filename(
        lemonDirectory,
        "lemonade.lemon"
    )
    
    with open(sourkeyFilePath, "rb") as file:
        magic = file.read(len(SOURKEY_MAGIC))

        if magic != SOURKEY_MAGIC:
            raise e.InvalidSourkeyFileError(
                "Invalid .sourkey file."
            )

        key_bytes = file.read()
    
    crypt_bytes = c.encrypt_with_key(data_bytes, key_bytes)
    
    with open(lemon_path, "wb") as file:
        file.write(LEMON_MAGIC)
        file.write(crypt_bytes)


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


def generate_sourkey_file(
    sourkeyPath: str,
    length: int
) -> None:
    """
    Generates a Lemonade .sourkey file containing a random encryption key.

    The function creates a cryptographically secure random key and stores it
    in the Lemonade sourkey file format.

    The generated file structure is:

        SOURKEY_MAGIC
        Key Bytes

    The SOURKEY_MAGIC sequence is used to identify the file as a valid
    Lemonade sourkey file.

    Args:
        sourkeyPath (str):
            Path where the .sourkey file will be created.

        length (int):
            Number of random bytes to generate for the key.

    Returns:
        None

    Raises:
        LemonadeError:
            When the provided path or key length is invalid.

        InvalidPathError:
            When the provided path is invalid.
    """

    if not isinstance(sourkeyPath, str):
        raise e.LemonadeError(
            ".sourkey file path must be a string."
        )

    if not isinstance(length, int):
        raise e.LemonadeError(
            "Key length must be an integer."
        )

    if length <= 0:
        raise e.LemonadeError(
            "Key length cannot be less than or equal to zero."
        )

    key_bytes = c.generate_key(length)

    with open(sourkeyPath, "wb") as file:
        file.write(SOURKEY_MAGIC)
        file.write(key_bytes)