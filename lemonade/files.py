import os

from . import crypto as c
from . import exceptions as e
from . import utils as u
from . import metadata as m

from .version import __version__


LEMON_MAGIC = b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x92"
SOURKEY_MAGIC = b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x91"

VERSION = __version__.encode("utf-8")

SUPPORTED_VERSIONS = [
    VERSION
]


def encrypt_to_file(
    filePath: str,
    lemonDirectory: str,
    sourkeyDirectory: str = ""
) -> None:
    """
    Encrypts a file and stores it in Lemonade files.

    Creates:
        - A .lemon file containing encrypted data.
        - A .sourkey file containing the encryption key.

    Args:
        filePath (str):
            Path to the file to encrypt.

        lemonDirectory (str):
            Directory where the .lemon file will be created.

        sourkeyDirectory (str, optional):
            Directory where the .sourkey file will be created.
            If empty, uses lemonDirectory.
    """

    if not isinstance(filePath, str):
        raise e.LemonadeError(
            "File path must be a string."
        )

    if not isinstance(lemonDirectory, str):
        raise e.LemonadeError(
            ".lemon directory path must be a string."
        )

    if not isinstance(sourkeyDirectory, str):
        raise e.LemonadeError(
            ".sourkey directory path must be a string."
        )

    if not os.path.isfile(filePath):
        raise e.InvalidPathError(
            "File path must be a valid file."
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

    with open(filePath, "rb") as file:
        data_bytes = file.read()

    lemon_path = u._get_available_filename(
        lemonDirectory,
        "lemonade.lemon"
    )

    sourkey_path = u._get_available_filename(
        sourkeyDirectory,
        "lemonade.sourkey"
    )

    metadata = m.generate_metadata_bytes(
        filePath
    )

    crypt_bytes, key_bytes = c.encrypt(
        data_bytes
    )

    with open(lemon_path, "wb") as file:
        file.write(LEMON_MAGIC)

        file.write(
            len(VERSION).to_bytes(
                2,
                "big"
            )
        )

        file.write(VERSION)

        file.write(
            len(metadata).to_bytes(
                4,
                "big"
            )
        )

        file.write(metadata)

        file.write(crypt_bytes)

    with open(sourkey_path, "wb") as file:
        file.write(SOURKEY_MAGIC)
        file.write(key_bytes)


def encrypt_with_sourkey_to_file(
    filePath: str,
    lemonDirectory: str,
    sourkeyFilePath: str
) -> None:
    """
    Encrypts a file using an existing .sourkey file.

    Creates:
        - A .lemon file containing encrypted data.

    Args:
        filePath (str):
            Path to the file to encrypt.

        lemonDirectory (str):
            Directory where the .lemon file will be created.

        sourkeyFilePath (str):
            Path to the existing .sourkey file.
    """

    if not isinstance(filePath, str):
        raise e.LemonadeError(
            "File path must be a string."
        )

    if not isinstance(lemonDirectory, str):
        raise e.LemonadeError(
            ".lemon directory path must be a string."
        )

    if not isinstance(sourkeyFilePath, str):
        raise e.LemonadeError(
            ".sourkey file path must be a string."
        )

    if not os.path.isfile(filePath):
        raise e.InvalidPathError(
            "File path must be a valid file."
        )

    if not os.path.isdir(lemonDirectory):
        raise e.InvalidPathError(
            ".lemon directory path must be a valid directory."
        )

    if not os.path.isfile(sourkeyFilePath):
        raise e.InvalidPathError(
            ".sourkey file path must be a valid file."
        )

    with open(filePath, "rb") as file:
        data_bytes = file.read()

    lemon_path = u._get_available_filename(
        lemonDirectory,
        "lemonade.lemon"
    )

    with open(sourkeyFilePath, "rb") as file:
        magic = file.read(
            len(SOURKEY_MAGIC)
        )

        if magic != SOURKEY_MAGIC:
            raise e.InvalidSourkeyFileError(
                "Invalid .sourkey file."
            )

        key_bytes = file.read()

    metadata = m.generate_metadata_bytes(
        filePath
    )

    crypt_bytes = c.encrypt_with_key(
        data_bytes,
        key_bytes
    )

    with open(lemon_path, "wb") as file:
        file.write(LEMON_MAGIC)

        file.write(
            len(VERSION).to_bytes(
                2,
                "big"
            )
        )

        file.write(VERSION)

        file.write(
            len(metadata).to_bytes(
                4,
                "big"
            )
        )

        file.write(metadata)

        file.write(crypt_bytes)
        

def decrypt_from_file(
    lemonFilePath: str,
    sourkeyFilePath: str,
    outputDirectory: str
) -> None:
    """
    Decrypts a Lemonade file and recreates the original file.

    Args:
        lemonFilePath (str):
            Path to the .lemon file.

        sourkeyFilePath (str):
            Path to the .sourkey file.

        outputDirectory (str):
            Directory where the restored file will be created.
    """

    if not isinstance(lemonFilePath, str):
        raise e.LemonadeError(
            ".lemon file path must be a string."
        )

    if not isinstance(sourkeyFilePath, str):
        raise e.LemonadeError(
            ".sourkey file path must be a string."
        )

    if not isinstance(outputDirectory, str):
        raise e.LemonadeError(
            "Output directory must be a string."
        )

    if not os.path.isfile(lemonFilePath):
        raise e.InvalidPathError(
            ".lemon file path must be a valid file."
        )

    if not os.path.isfile(sourkeyFilePath):
        raise e.InvalidPathError(
            ".sourkey file path must be a valid file."
        )

    if not os.path.isdir(outputDirectory):
        raise e.InvalidPathError(
            "Output directory must be a valid directory."
        )

    with open(lemonFilePath, "rb") as file:

        magic = file.read(
            len(LEMON_MAGIC)
        )

        if magic != LEMON_MAGIC:
            raise e.InvalidLemonFileError(
                "Invalid .lemon file."
            )


        version_size_bytes = file.read(2)

        if len(version_size_bytes) != 2:
            raise e.InvalidLemonFileError(
                "Invalid version header."
            )

        version_size = int.from_bytes(
            version_size_bytes,
            "big"
        )

        file_version = file.read(
            version_size
        )

        if len(file_version) != version_size:
            raise e.InvalidLemonFileError(
                "Invalid version data."
            )

        if file_version not in SUPPORTED_VERSIONS:
            raise e.UnsupportedVersionError(
                "Unsupported Lemonade file version."
            )


        metadata_size_bytes = file.read(4)

        if len(metadata_size_bytes) != 4:
            raise e.InvalidLemonFileError(
                "Invalid metadata header."
            )

        metadata_size = int.from_bytes(
            metadata_size_bytes,
            "big"
        )

        metadata_bytes = file.read(
            metadata_size
        )

        if len(metadata_bytes) != metadata_size:
            raise e.InvalidLemonFileError(
                "Incomplete metadata section."
            )

        fields = m.read_metadata(
            metadata_bytes
        )

        crypt_bytes = file.read()


    with open(sourkeyFilePath, "rb") as file:

        magic = file.read(
            len(SOURKEY_MAGIC)
        )

        if magic != SOURKEY_MAGIC:
            raise e.InvalidSourkeyFileError(
                "Invalid .sourkey file."
            )

        key_bytes = file.read()


    data_bytes = c.decrypt(
        crypt_bytes,
        key_bytes
    )


    filename_bytes = u._get_metadata_field(
        fields,
        m.MetadataType.FILENAME
    )

    if filename_bytes is None:
        raise e.InvalidMetadataError(
            "Filename metadata not found."
        )


    filename = filename_bytes.decode(
        "utf-8"
    )

    filename = os.path.basename(
        filename
    )


    output_path = os.path.join(
        outputDirectory,
        filename
    )


    with open(output_path, "wb") as file:
        file.write(data_bytes)


def generate_sourkey_file(
    sourkeyPath: str,
    length: int
) -> None:
    """
    Generates a Lemonade .sourkey file containing a random encryption key.

    Args:
        sourkeyPath (str):
            Path where the .sourkey file will be created.

        length (int):
            Number of bytes in the generated key.
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