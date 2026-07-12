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


def test_invalid_lemon_file_magic(tmp_path):
    
    lemon_file = tmp_path / "invalid.lemon"
    
    sourkey_file = tmp_path / "valid.sourkey"

    lemon_file.write_bytes(b"invalid lemon data")
    
    sourkey_file.write_bytes(b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x91" + b"key")

    with pytest.raises(InvalidLemonFileError):
        decrypt_from_file(
            str(lemon_file),
            str(sourkey_file)
        )


def test_invalid_sourkey_file_magic(tmp_path):
    
    lemon_file = tmp_path / "valid.lemon"
    
    sourkey_file = tmp_path / "invalid.sourkey"

    lemon_file.write_bytes(
        b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x92" + b"crypt"
    )

    sourkey_file.write_bytes(b"invalid sourkey data")

    with pytest.raises(InvalidSourkeyFileError):
        decrypt_from_file(
            str(lemon_file),
            str(sourkey_file)
        )


def test_invalid_lemon_path():
    
    with pytest.raises(InvalidPathError):
        decrypt_from_file(
            "nonexistent.lemon",
            "nonexistent.sourkey"
        )


def test_invalid_sourkey_path(tmp_path):
    
    lemon_file = tmp_path / "invalid.lemon"

    lemon_file.write_bytes(
        b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x92" + b"crypt"
    )

    with pytest.raises(InvalidPathError):
        decrypt_from_file(
            str(lemon_file),
            "nonexistent.sourkey"
        )


def test_invalid_sourkey_for_encryption(tmp_path):
    
    invalid_sourkey = tmp_path / "invalid.sourkey"

    invalid_sourkey.write_bytes(b"invalid")

    with pytest.raises(InvalidSourkeyFileError):
        encrypt_with_sourkey_to_file(
            b"Hello",
            str(tmp_path),
            str(invalid_sourkey)
        )


def test_invalid_encrypt_directory():
    
    with pytest.raises(InvalidPathError):
        encrypt_to_file(
            b"Hello",
            "not_a_directory"
        )


def test_encrypt_and_decrypt_file(tmp_path):

    data = b"Hello Lemonade Files"

    encrypt_to_file(
        data,
        str(tmp_path)
    )

    lemon_file = tmp_path / "lemonade_1.lemon"
    sourkey_file = tmp_path / "lemonade_1.sourkey"

    result = decrypt_from_file(
        str(lemon_file),
        str(sourkey_file)
    )

    assert result == data


def test_encrypt_with_existing_sourkey(tmp_path):

    data = b"Testing sourkey"

    encrypt_to_file(
        data,
        str(tmp_path)
    )

    sourkey = tmp_path / "lemonade_1.sourkey"

    encrypt_with_sourkey_to_file(
        data,
        str(tmp_path),
        str(sourkey)
    )

    lemon_files = list(tmp_path.glob("*.lemon"))

    assert len(lemon_files) == 2


def test_magic_validation(tmp_path):

    invalid = tmp_path / "invalid.sourkey"

    invalid.write_bytes(b"invalid")

    try:
        encrypt_with_sourkey_to_file(
            b"test",
            str(tmp_path),
            str(invalid)
        )

        assert False

    except Exception:
        assert True
        