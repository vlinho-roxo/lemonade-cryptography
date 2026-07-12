import secrets

from . import exceptions as e


def encrypt(
    data_bytes: bytes
) -> tuple[bytes, bytes]:
    """
    Encrypts binary data using Lemonade Encryption.

    Generates a random key with the same length as the input data and
    performs byte-wise modular subtraction.

    The encryption formula is:

        C = (M - K) mod 256

    Where:
        C = encrypted byte
        M = message byte
        K = key byte

    Args:
        data_bytes (bytes): Data to be encrypted.

    Returns:
        tuple[bytes, bytes]:
            A tuple containing:
            - The encrypted data.
            - The encryption key.

    Raises:
        LemonadeError:
            When the input data is invalid.
    """

    if not isinstance(data_bytes, bytes):
        raise e.LemonadeError(
            "Message must be bytes."
        )

    key_bytes = secrets.token_bytes(len(data_bytes))

    crypt_bytes = bytes(
        (data_bytes[i] - key_bytes[i]) % 256
        for i in range(len(data_bytes))
    )

    return crypt_bytes, key_bytes


def decrypt(
    crypt_bytes: bytes,
    key_bytes: bytes
) -> bytes:
    """
    Decrypts binary data encrypted with Lemonade Encryption.

    Uses the original encryption key to restore the original data.

    The decryption formula is:

        M = (C + K) mod 256

    Where:
        M = original message byte
        C = encrypted byte
        K = key byte

    Args:
        crypt_bytes (bytes):
            Encrypted data.

        key_bytes (bytes):
            Encryption key generated during encryption.

    Returns:
        bytes:
            The original decrypted data.

    Raises:
        InvalidCipherError:
            When the encrypted data is invalid.

        InvalidKeyError:
            When the key is invalid or has an incompatible length.

        LemonadeError:
            When decryption fails.
    """

    if not isinstance(crypt_bytes, bytes):
        raise e.InvalidCipherError(
            "Cipher must be bytes."
        )

    if not isinstance(key_bytes, bytes):
        raise e.InvalidKeyError(
            "Key must be bytes."
        )

    if len(crypt_bytes) != len(key_bytes):
        raise e.InvalidKeyError(
            "Encryption key length does not match cipher length."
        )

    try:
        data_bytes = bytes(
            (crypt_bytes[i] + key_bytes[i]) % 256
            for i in range(len(crypt_bytes))
        )
    except IndexError as error:
        raise e.LemonadeError(
            "Error while decrypting cipher."
        ) from error

    return data_bytes