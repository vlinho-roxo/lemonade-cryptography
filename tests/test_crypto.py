import pytest
from lemonade import encrypt, decrypt
from lemonade.exceptions import InvalidKeyError


def test_invalid_key():
    with pytest.raises(InvalidKeyError):
        decrypt("YWJj", "invalid")
        
        
def test_basic_encryption():
    message = "Hello Lemonade"
    crypt, key = encrypt(message)
    result = decrypt(crypt, key)

    assert result == message


def test_unicode():
    message = "🍋 Se a vida te der limões, faça uma limonada >w< 世界"
    crypt, key = encrypt(message)

    assert decrypt(crypt, key) == message
    
    
def test_long_message():
    message = "LIMÃO" * 2000
    crypt, key = encrypt(message)

    assert decrypt(crypt, key) == message
    

def test_empty_message():
    message = ""
    crypt, key = encrypt(message)

    assert decrypt(crypt, key) == message
    
