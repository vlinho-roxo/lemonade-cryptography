import os
import hashlib

from . import crypto as c
from . import exceptions as e
from . import utils as u
from . import metadata as m
from . import constants as const


def encrypt_to_file(filePath: str, lemonDirectory: str, sourkeyDirectory: str = "") -> None:
    """
    [DEPRECATED] Encrypts a file and stores it in Lemonade files.

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
        raise e.LemonadeError("File path must be a string.")

    if not isinstance(lemonDirectory, str):
        raise e.LemonadeError(".lemon directory path must be a string.")

    if not isinstance(sourkeyDirectory, str):
        raise e.LemonadeError(".sourkey directory path must be a string.")

    if not os.path.isfile(filePath):
        raise e.InvalidPathError("File path must be a valid file.")

    if not os.path.isdir(lemonDirectory):
        raise e.InvalidPathError(".lemon directory path must be a valid directory.")

    if sourkeyDirectory != "" and not os.path.isdir(sourkeyDirectory):
        raise e.InvalidPathError(".sourkey directory path must be a valid directory.")

    if sourkeyDirectory == "":
        sourkeyDirectory = lemonDirectory

    lemon_path = u._get_available_filename(lemonDirectory, "lemonade.lemon")
    sourkey_path = u._get_available_filename(sourkeyDirectory, "lemonade.sourkey")
    metadata = m.generate_metadata_bytes(filePath)

    with open(filePath, "rb") as input_file:
        with open(lemon_path, "wb") as lemon_file:
            with open(sourkey_path, "wb") as sourkey_file:

                lemon_file.write(const.LEMON_MAGIC)
                lemon_file.write(len(const.VERSION).to_bytes(2, "big"))
                lemon_file.write(const.VERSION)
                lemon_file.write(len(metadata).to_bytes(4, "big"))
                lemon_file.write(metadata)

                sourkey_file.write(const.SOURKEY_MAGIC)
                
                data_chunk = input_file.read(const.CHUNK_SIZE)

                while data_chunk:
                    crypt_chunk, key_chunk = c.encrypt(data_chunk)

                    lemon_file.write(crypt_chunk)
                    sourkey_file.write(key_chunk)

                    data_chunk = input_file.read(const.CHUNK_SIZE)


def encrypt_with_sourkey_to_file(filePath: str, lemonDirectory: str, sourkeyFilePath: str) -> None:
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
        raise e.LemonadeError("File path must be a string.")

    if not isinstance(lemonDirectory, str):
        raise e.LemonadeError(".lemon directory path must be a string.")

    if not isinstance(sourkeyFilePath, str):
        raise e.LemonadeError(".sourkey file path must be a string.")

    if not os.path.isfile(filePath):
        raise e.InvalidPathError("File path must be a valid file.")

    if not os.path.isdir(lemonDirectory):
        raise e.InvalidPathError(".lemon directory path must be a valid directory.")

    if not os.path.isfile(sourkeyFilePath):
        raise e.InvalidPathError(".sourkey file path must be a valid file.")

    lemon_path = u._get_available_filename(lemonDirectory, "lemonade.lemon")
    metadata = m.generate_metadata_bytes(filePath)

    with open(sourkeyFilePath, "rb") as sourkey_file:
        if sourkey_file.read(len(const.SOURKEY_MAGIC)) != const.SOURKEY_MAGIC:
            raise e.InvalidSourkeyFileError("Invalid .sourkey file.")

        with open(filePath, "rb") as input_file, open(lemon_path, "wb") as lemon_file:
            lemon_file.write(const.LEMON_MAGIC)
            lemon_file.write(len(const.VERSION).to_bytes(2, "big"))
            lemon_file.write(const.VERSION)
            lemon_file.write(len(metadata).to_bytes(4, "big"))
            lemon_file.write(metadata)

            data_chunk = input_file.read(const.CHUNK_SIZE)

            while data_chunk:
                key_chunk = sourkey_file.read(len(data_chunk))

                if len(key_chunk) != len(data_chunk):
                    raise e.InvalidSourkeyFileError("Sourkey is shorter than the input file.")

                crypt_chunk = c.encrypt_with_key(data_chunk, key_chunk)
                lemon_file.write(crypt_chunk)

                data_chunk = input_file.read(const.CHUNK_SIZE)
        

def decrypt_from_file(lemonFilePath: str, sourkeyFilePath: str, outputDirectory: str) -> None:
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
        raise e.LemonadeError(".lemon file path must be a string.")

    if not isinstance(sourkeyFilePath, str):
        raise e.LemonadeError(".sourkey file path must be a string.")

    if not isinstance(outputDirectory, str):
        raise e.LemonadeError("Output directory must be a string.")

    if not os.path.isfile(lemonFilePath):
        raise e.InvalidPathError(".lemon file path must be a valid file.")

    if not os.path.isfile(sourkeyFilePath):
        raise e.InvalidPathError(".sourkey file path must be a valid file.")

    if not os.path.isdir(outputDirectory):
        raise e.InvalidPathError("Output directory must be a valid directory.")

    with open(lemonFilePath, "rb") as lemon_file:
        if lemon_file.read(len(const.LEMON_MAGIC)) != const.LEMON_MAGIC:
            raise e.InvalidLemonFileError("Invalid .lemon file.")

        version_size_bytes = lemon_file.read(2)

        if len(version_size_bytes) != 2:
            raise e.InvalidLemonFileError("Invalid version header.")

        version_size = int.from_bytes(version_size_bytes, "big")
        file_version = lemon_file.read(version_size)

        if len(file_version) != version_size:
            raise e.InvalidLemonFileError("Invalid version data.")

        if file_version not in const.SUPPORTED_VERSIONS:
            raise e.UnsupportedVersionError("Unsupported Lemonade file version.")

        metadata_size_bytes = lemon_file.read(4)

        if len(metadata_size_bytes) != 4:
            raise e.InvalidLemonFileError("Invalid metadata header.")

        metadata_size = int.from_bytes(metadata_size_bytes, "big")
        metadata_bytes = lemon_file.read(metadata_size)

        if len(metadata_bytes) != metadata_size:
            raise e.InvalidLemonFileError("Incomplete metadata section.")

        fields = m.read_metadata(metadata_bytes)

        chunk_size_bytes = u._get_metadata_field(fields, m.MetadataType.CHUNKSIZE)

        if chunk_size_bytes is None:
            raise e.InvalidMetadataError("Chunk size metadata not found.")

        chunk_size = int.from_bytes(chunk_size_bytes, "little")

        filename_bytes = u._get_metadata_field(fields, m.MetadataType.FILENAME)

        if filename_bytes is None:
            raise e.InvalidMetadataError("Filename metadata not found.")

        filename = os.path.basename(filename_bytes.decode("utf-8"))
        output_path = os.path.join(outputDirectory, filename)

        original_hash = u._get_metadata_field(fields, m.MetadataType.SHA256)

        if original_hash is None:
            raise e.InvalidMetadataError("SHA256 metadata not found.")
        
        sha256 = hashlib.sha256()

        with open(sourkeyFilePath, "rb") as sourkey_file:
            if sourkey_file.read(len(const.SOURKEY_MAGIC)) != const.SOURKEY_MAGIC:
                raise e.InvalidSourkeyFileError("Invalid .sourkey file.")

            with open(output_path, "wb") as output_file:
                while True:
                    crypt_chunk = lemon_file.read(chunk_size)

                    if not crypt_chunk:
                        break

                    key_chunk = sourkey_file.read(len(crypt_chunk))

                    if len(key_chunk) != len(crypt_chunk):
                        raise e.InvalidSourkeyFileError("Sourkey is shorter than the encrypted data.")

                    data_chunk = c.decrypt(crypt_chunk, key_chunk)

                    output_file.write(data_chunk)
                    sha256.update(data_chunk)

        if sha256.digest() != original_hash:
            raise e.IntegrityError("File integrity verification failed.")


def generate_sourkey_file(sourkeyPath: str, length: int) -> None:
    """
    Generates a Lemonade .sourkey file containing a random encryption key.

    Args:
        sourkeyPath (str):
            Path where the .sourkey file will be created.

        length (int):
            Number of bytes in the generated key.
    """

    if not isinstance(sourkeyPath, str):
        raise e.LemonadeError(".sourkey file path must be a string.")

    if not isinstance(length, int):
        raise e.LemonadeError("Key length must be an integer.")

    if length <= 0:
        raise e.LemonadeError("Key length cannot be less than or equal to zero.")

    key_bytes = c.generate_key(length)

    with open(sourkeyPath, "wb") as file:
        file.write(const.SOURKEY_MAGIC)
        file.write(key_bytes)