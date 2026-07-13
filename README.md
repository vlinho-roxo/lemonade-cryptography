# 🍋 Lemonade Cryptography

**Lemonade Cryptography** is a lightweight byte-oriented encryption library based on modular arithmetic and symmetric key transformations.

Lemonade transforms binary data into encrypted data by applying mathematical operations between data bytes and cryptographic key bytes.

The core concept is:

> Each byte of the data is encrypted using a corresponding byte from a secret key.

The original data can be recovered by applying the reverse operation using the same key.

Lemonade also provides encrypted file processing through its own file formats:

* `.lemon` — encrypted data container
* `.sourkey` — separated encryption key storage

Encrypted files include metadata information and SHA-256 integrity verification.

---

# Installation

Install Lemonade Cryptography using pip:

```bash
pip install lemonade-cryptography
```

---

# Quick Start

```python
from lemonade import encrypt, decrypt

message = b"Hello Lemonade!"

crypt, key = encrypt(message)

print("Encrypted:")
print(crypt)

print("\nKey:")
print(key)

original = decrypt(crypt, key)

print("\nDecrypted:")
print(original)
```

Output:

```
Encrypted:
<encrypted bytes>

Key:
<secret key bytes>

Decrypted:
b'Hello Lemonade!'
```

---

# Features

* Symmetric key encryption
* Byte-oriented processing
* UTF-8 compatible through byte conversion
* Random cryptographic key generation
* Custom key encryption
* `.lemon` encrypted file format
* `.sourkey` key file format
* File metadata storage
* SHA-256 integrity verification
* Automatic filename restoration after decryption
* Version validation for encrypted files
* Lightweight Python API

---

# API Reference

## `encrypt()`

```python
encrypt(data_bytes: bytes) -> tuple[bytes, bytes]
```

Encrypts binary data and generates a random key with the same length as the input data.

### Arguments

| Argument     | Type    | Description     |
| ------------ | ------- | --------------- |
| `data_bytes` | `bytes` | Data to encrypt |

### Returns

A tuple containing:

```python
(
    encrypted_data,
    encryption_key
)
```

Example:

```python
crypt, key = encrypt(b"Hello")
```

---

## `encrypt_with_key()`

```python
encrypt_with_key(
    data_bytes: bytes,
    key_bytes: bytes
) -> bytes
```

Encrypts binary data using an existing key.

If the key is shorter than the data, the key bytes are repeated cyclically.

Example:

```
Data:
ABCDEFG

Key:
XYZ

Used key:
XYZXYZX
```

### Arguments

| Argument     | Type    | Description             |
| ------------ | ------- | ----------------------- |
| `data_bytes` | `bytes` | Data to encrypt         |
| `key_bytes`  | `bytes` | Existing encryption key |

### Returns

Encrypted data:

```python
bytes
```

---

## `decrypt()`

```python
decrypt(
    crypt_bytes: bytes,
    key_bytes: bytes
) -> bytes
```

Decrypts Lemonade encrypted data using its key.

### Returns

The original data:

```python
bytes
```

---

## `generate_key()`

```python
generate_key(length: int) -> bytes
```

Generates a cryptographically secure random key.

### Arguments

| Argument | Type  | Description     |
| -------- | ----- | --------------- |
| `length` | `int` | Number of bytes |

### Returns

Generated key:

```python
bytes
```

---

# File Processing

Lemonade provides encrypted file containers.

## `.lemon`

A `.lemon` file stores encrypted data, metadata, and format information.

Structure:

```
LEMON_MAGIC
VERSION
METADATA_SIZE
METADATA
ENCRYPTED_DATA
```

The metadata section stores:

* Original filename
* File extension
* Original file size
* Last modification timestamp
* SHA-256 integrity hash

---

## `.sourkey`

A `.sourkey` file stores the encryption key separately.

Structure:

```
SOURKEY_MAGIC
KEY_BYTES
```

A `.sourkey` file can be reused to encrypt multiple files.

---

# File API

## `encrypt_to_file()`

```python
encrypt_to_file(
    filePath: str,
    lemonDirectory: str,
    sourkeyDirectory: str = ""
) -> None
```

Encrypts a file and creates:

* A `.lemon` encrypted file
* A `.sourkey` key file

Example:

```python
encrypt_to_file(
    "document.pdf",
    "encrypted/"
)
```

---

## `encrypt_with_sourkey_to_file()`

```python
encrypt_with_sourkey_to_file(
    filePath: str,
    lemonDirectory: str,
    sourkeyFilePath: str
) -> None
```

Encrypts a file using an existing `.sourkey`.

Example:

```python
encrypt_with_sourkey_to_file(
    "image.png",
    "encrypted/",
    "mykey.sourkey"
)
```

---

## `decrypt_from_file()`

```python
decrypt_from_file(
    lemonFilePath: str,
    sourkeyFilePath: str,
    outputDirectory: str
) -> None
```

Decrypts a `.lemon` file and recreates the original file.

The original filename is restored automatically from metadata.

During decryption, Lemonade verifies the SHA-256 hash stored in metadata.

If the data was modified or corrupted:

```python
IntegrityError
```

is raised.

Example:

```python
decrypt_from_file(
    "document.lemon",
    "document.sourkey",
    "output/"
)
```

---

## `generate_sourkey_file()`

```python
generate_sourkey_file(
    sourkeyPath: str,
    length: int
) -> None
```

Creates a new `.sourkey` file containing a random key.

Example:

```python
generate_sourkey_file(
    "key.sourkey",
    32
)
```

---

# How It Works

Lemonade operates directly on byte values.

The encryption operation is:

```
C = (M - K) mod 256
```

Where:

| Symbol | Meaning            |
| ------ | ------------------ |
| `C`    | Encrypted byte     |
| `M`    | Original data byte |
| `K`    | Key byte           |

The decryption operation reverses the transformation:

```
M = (C + K) mod 256
```

More technical details can be found in:

```
docs/algorithm.md
```

---

# Integrity Verification

Lemonade stores a SHA-256 hash of the original data inside the metadata section.

During decryption:

1. Data is decrypted.
2. SHA-256 is calculated again.
3. The calculated hash is compared with the stored hash.

If both hashes match, the file is considered intact.

If they differ, Lemonade raises an integrity error.

---

# Security Notice

Lemonade Cryptography is an experimental encryption library created for educational purposes and lightweight applications.

It is not intended to replace modern cryptographic standards such as AES or ChaCha20 in security-critical systems.

Always protect your encryption keys. Without the correct key, encrypted data cannot be recovered.

SHA-256 integrity verification detects accidental corruption and modifications, but it does not provide authentication against advanced attackers.

---

# License

Lemonade Cryptography is licensed under the MIT License.
