import pytest

from lemonade.files import (
    encrypt_to_file,
    decrypt_from_file,
    encrypt_with_sourkey_to_file
)

from lemonade.exceptions import (
    InvalidPathError,
    InvalidLemonFileError,
    InvalidSourkeyFileError
)


def test_encrypt_and_decrypt_file(tmp_path):

    original_content = b"Hello Lemonade!"

    original_file = tmp_path / "hello.txt"

    with open(original_file, "wb") as file:
        file.write(original_content)

    encrypt_to_file(
        str(original_file),
        str(tmp_path)
    )

    lemon_file = None
    sourkey_file = None

    for file in os.listdir(tmp_path):
        if file.endswith(".lemon"):
            lemon_file = tmp_path / file

        if file.endswith(".sourkey"):
            sourkey_file = tmp_path / file

    assert lemon_file is not None
    assert sourkey_file is not None

    decrypted = decrypt_from_file(
        str(lemon_file),
        str(sourkey_file)
    )

    assert decrypted == original_content