import base64
import binascii
import secrets

from . import exceptions as e


def encrypt(msg: str) -> tuple[str, str]:
    """Encrypts a message using Lemonade Encryption.

    Generates a random key with the same byte length as the message.

    Args:
        msg (str): Text to be encrypted.

    Returns:
        tuple[str, str]: Encrypted message and its key.

    Raises:
        LemonadeError: When the message is invalid.
    """

    if not isinstance(msg, str):
        raise e.LemonadeError("Message must be a string.")

    try:
        msg_bytes = msg.encode("utf-8")
    except UnicodeEncodeError as error:
        raise e.LemonadeError(
            "Unable to encode message as UTF-8."
        ) from error

    key_bytes = secrets.token_bytes(len(msg_bytes))

    crypt_bytes = bytes(
        (msg_bytes[i] - key_bytes[i]) % 256
        for i in range(len(msg_bytes))
    )

    crypt = base64.b64encode(crypt_bytes).decode("ascii")
    key = base64.b64encode(key_bytes).decode("ascii")

    return crypt, key


def decrypt(crypt: str, key: str) -> str:
    """Decrypts a Lemonade encrypted message.

    Args:
        crypt (str): Encrypted message in Base64.
        key (str): Encryption key in Base64.

    Returns:
        str: Decrypted original message.

    Raises:
        InvalidCipherError: When the encrypted message is invalid.
        InvalidKeyError: When the key is invalid.
        LemonadeError: When decryption fails.
    """

    if not isinstance(crypt, str):
        raise e.InvalidCipherError(
            "Cipher must be a string."
        )

    if not isinstance(key, str):
        raise e.InvalidKeyError(
            "Key must be a string."
        )

    try:
        crypt_bytes = base64.b64decode(
            crypt,
            validate=True
        )
    except (binascii.Error, ValueError) as error:
        raise e.InvalidCipherError(
            "Invalid cryptography."
        ) from error

    try:
        key_bytes = base64.b64decode(
            key,
            validate=True
        )
    except (binascii.Error, ValueError) as error:
        raise e.InvalidKeyError(
            "Invalid encryption key."
        ) from error

    if len(key_bytes) != len(crypt_bytes):
        raise e.InvalidKeyError(
            "Encryption key length does not match cipher length."
        )

    try:
        msg_bytes = bytes(
            (crypt_bytes[i] + key_bytes[i]) % 256
            for i in range(len(crypt_bytes))
        )
    except IndexError as error:
        raise e.LemonadeError(
            "Error while decrypting cipher."
        ) from error

    try:
        return msg_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise e.LemonadeError(
            "Decrypted data is not valid UTF-8."
        ) from error