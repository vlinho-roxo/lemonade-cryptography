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
            "Data must be bytes."
        )

    key_bytes = generate_key(len(data_bytes))

    crypt_bytes = encrypt_with_key(data_bytes, key_bytes)

    return crypt_bytes, key_bytes


def encrypt_with_key(
    data_bytes: bytes,
    key_bytes: bytes
) -> bytes:
    """
    Encrypts binary data using a provided key.

    Lemonade Encryption performs byte-wise modular subtraction:

        C = (M - K) mod 256

    If the provided key is shorter than the data, the key bytes are
    repeated cyclically until the complete data length is reached.

    Example:

        Data:
        ABCDEFG

        Key:
        XYZ

        Used key:
        XYZXYZX


    Args:
        data_bytes (bytes):
            Binary data to encrypt.

        key_bytes (bytes):
            Encryption key.

    Returns:
        bytes:
            Encrypted data.

    Raises:
        LemonadeError:
            When data or key are invalid.
    """

    if not isinstance(data_bytes, bytes):
        raise e.LemonadeError(
            "Data must be bytes."
        )
        
    if not isinstance(key_bytes, bytes):
        raise e.LemonadeError(
            "Key must be bytes."
        )

    if len(key_bytes) == 0:
        raise e.LemonadeError(
            "Key cannot be empty."
        )
        
    crypt_bytes = bytes(
        (
            data_bytes[i] - key_bytes[i % len(key_bytes)]
        ) % 256
        for i in range(len(data_bytes))
    )
    
    return crypt_bytes


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


def generate_key(
    length: int
) -> bytes:
    """
    Generates a random encryption key.

    The generated key consists of cryptographically secure random bytes
    using Python's secrets module.

    Args:
        length (int):
            Number of bytes to generate.

    Returns:
        bytes:
            Randomly generated key.

    Raises:
        LemonadeError:
            When the length is invalid.
    """

    if not isinstance(length, int):
        raise e.LemonadeError(
            "Length must be integer."
        )
        
    if length <= 0:
        raise e.LemonadeError(
            "Length cannot be less than or equal to zero."
        )
        
    return secrets.token_bytes(length)