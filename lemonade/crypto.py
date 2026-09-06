import secrets

from . import exceptions as e
from .data_sctructures.queue import Queue
from .data_sctructures.linked_list import LinkedList 

CHUNK_SIZE = 1024 * 1024

def encrypt(data_bytes: bytes) -> tuple[bytes, bytes]:
    """
    [DEPRECATED] Encrypts binary data using Lemonade Encryption.

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


def encrypt_with_key(data_bytes: bytes, key_bytes: bytes) -> bytes:
    """
    [DEPRECATED] Encrypts binary data using a provided key.

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
        raise e.LemonadeError("Data must be bytes.")

    if not isinstance(key_bytes, bytes):
        raise e.LemonadeError("Key must be bytes.")

    if len(key_bytes) == 0:
        raise e.LemonadeError("Key cannot be empty.")

    data_chunks = LinkedList()
    key_chunks = LinkedList()

    for i in range(0, len(data_bytes), CHUNK_SIZE):
        data_queue = Queue()

        for byte in data_bytes[i:i + CHUNK_SIZE]:
            data_queue.enqueue(byte)

        data_chunks.insert_at_end(data_queue)

    key_index = 0

    for i in range(0, len(data_bytes), CHUNK_SIZE):
        key_queue = Queue()

        chunk_size = min(CHUNK_SIZE, len(data_bytes) - i)

        for _ in range(chunk_size):
            key_queue.enqueue(key_bytes[key_index])
            key_index += 1

            if key_index >= len(key_bytes):
                key_index = 0

        key_chunks.insert_at_end(key_queue)

    crypt_bytes = bytearray()
    
    data_node = data_chunks.first
    key_node = key_chunks.first

    while data_node is not None:

        data_queue = data_node.data
        key_queue = key_node.data

        while not data_queue.is_empty:

            data_byte = data_queue.dequeue()
            key_byte = key_queue.dequeue()

            crypt_bytes.append((data_byte - key_byte) % 256)

        data_node = data_node.next
        key_node = key_node.next

    crypt_bytes = bytes(crypt_bytes)

    return crypt_bytes


def decrypt(crypt_bytes: bytes, key_bytes: bytes) -> bytes:
    """
    [DEPRECATED] Decrypts binary data encrypted with Lemonade Encryption.

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
        raise e.InvalidCipherError("Cipher must be bytes.")

    if not isinstance(key_bytes, bytes):
        raise e.InvalidKeyError("Key must be bytes.")

    if len(key_bytes) == 0:
        raise e.InvalidKeyError("Key cannot be empty.")

    try:
        data_chunks = LinkedList()
        key_chunks = LinkedList()

        for i in range(0, len(crypt_bytes), CHUNK_SIZE):
            crypt_queue = Queue()

            for byte in crypt_bytes[i:i + CHUNK_SIZE]:
                crypt_queue.enqueue(byte)

            data_chunks.insert_at_end(crypt_queue)

        key_index = 0

        for i in range(0, len(crypt_bytes), CHUNK_SIZE):
            key_queue = Queue()
            chunk_size = min(CHUNK_SIZE, len(crypt_bytes) - i)

            for _ in range(chunk_size):
                key_queue.enqueue(key_bytes[key_index])
                key_index += 1

                if key_index >= len(key_bytes):
                    key_index = 0

            key_chunks.insert_at_end(key_queue)

        data_bytes = bytearray()

        data_node = data_chunks.first
        key_node = key_chunks.first

        while data_node is not None:
            crypt_queue = data_node.data
            key_queue = key_node.data

            while not crypt_queue.is_empty:
                crypt_byte = crypt_queue.dequeue()
                key_byte = key_queue.dequeue()

                data_bytes.append((crypt_byte + key_byte) % 256)

            data_node = data_node.next
            key_node = key_node.next

        return bytes(data_bytes)

    except IndexError as error:
        raise e.LemonadeError("Error while decrypting cipher.") from error


def generate_key(length: int) -> bytes:
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
        raise e.LemonadeError("Length must be integer.")
        
    if length <= 0:
        raise e.LemonadeError("Length cannot be less than or equal to zero.")
        
    return secrets.token_bytes(length)