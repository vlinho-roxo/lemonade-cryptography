import os

import pytest

from lemonade.files import (
    encrypt_to_file,
    decrypt_from_file
)

from lemonade import exceptions as e


def get_generated_files(directory):
    lemon_file = None
    sourkey_file = None

    for file in os.listdir(directory):
        if file.endswith(".lemon"):
            lemon_file = directory / file

        if file.endswith(".sourkey"):
            sourkey_file = directory / file

    return lemon_file, sourkey_file


def test_encrypt_and_decrypt_file(tmp_path):

    original_content = b"Hello Lemonade!"

    original_file = tmp_path / "hello.txt"

    with open(original_file, "wb") as file:
        file.write(original_content)


    encrypt_to_file(
        str(original_file),
        str(tmp_path)
    )


    lemon_file, sourkey_file = get_generated_files(
        tmp_path
    )


    assert lemon_file is not None
    assert sourkey_file is not None


    output_directory = tmp_path / "output"
    output_directory.mkdir()


    decrypt_from_file(
        str(lemon_file),
        str(sourkey_file),
        str(output_directory)
    )


    decrypted_file = output_directory / "hello.txt"

    assert decrypted_file.exists()


    with open(decrypted_file, "rb") as file:
        decrypted_content = file.read()


    assert decrypted_content == original_content



def test_integrity_check_detects_corrupted_file(tmp_path):

    original_content = b"Integrity test"

    original_file = tmp_path / "test.txt"

    with open(original_file, "wb") as file:
        file.write(original_content)


    encrypt_to_file(
        str(original_file),
        str(tmp_path)
    )


    lemon_file, sourkey_file = get_generated_files(
        tmp_path
    )


    with open(lemon_file, "r+b") as file:
        file.seek(-1, os.SEEK_END)

        byte = file.read(1)

        corrupted = bytes(
            [byte[0] ^ 0xFF]
        )

        file.seek(-1, os.SEEK_END)
        file.write(corrupted)


    output_directory = tmp_path / "output"
    output_directory.mkdir()


    with pytest.raises(e.IntegrityError):
        decrypt_from_file(
            str(lemon_file),
            str(sourkey_file),
            str(output_directory)
        )



def test_metadata_contains_sha256(tmp_path):

    original_file = tmp_path / "hash.txt"

    with open(original_file, "wb") as file:
        file.write(b"SHA256 TEST")


    encrypt_to_file(
        str(original_file),
        str(tmp_path)
    )


    lemon_file, _ = get_generated_files(
        tmp_path
    )


    with open(lemon_file, "rb") as file:

        file.seek(
            len(b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x92")
        )

        version_size = int.from_bytes(
            file.read(2),
            "big"
        )

        file.read(version_size)

        metadata_size = int.from_bytes(
            file.read(4),
            "big"
        )

        metadata = file.read(
            metadata_size
        )


    from lemonade.metadata import read_metadata
    from lemonade.metadata_type import MetadataType


    fields = read_metadata(metadata)

    sha256_field = None

    for field in fields:
        if field.identifier == MetadataType.SHA256:
            sha256_field = field


    assert sha256_field is not None
    assert len(sha256_field.data) == 32