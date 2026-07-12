import pytest

from lemonade import encrypt, decrypt
from lemonade.exceptions import InvalidKeyError


def test_invalid_key():
    with pytest.raises(InvalidKeyError):
        decrypt(b"abc", b"")


def test_basic_encryption():
    message = b"Hello Lemonade"

    crypt, key = encrypt(message)

    result = decrypt(crypt, key)

    assert result == message


def test_binary_data():

    data = bytes(range(256))

    crypt, key = encrypt(data)

    assert decrypt(crypt, key) == data


def test_long_data():

    data = b"LEMON" * 2000

    crypt, key = encrypt(data)

    assert decrypt(crypt, key) == data


def test_empty_data():

    data = b""

    crypt, key = encrypt(data)

    assert decrypt(crypt, key) == data