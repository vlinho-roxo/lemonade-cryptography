# 🍋 Lemonade Cryptography

**Lemonade Cryptography** is a lightweight byte-oriented encryption library based on modular arithmetic and symmetric key transformations.

Lemonade transforms binary data into encrypted data by applying mathematical operations between data bytes and cryptographic key bytes.

The core concept is:

> Each byte of the data is encrypted by subtracting it from a corresponding byte of a secret key.

The original data can be recovered by applying the reverse operation using the same key.

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

message = b"Hello. We are looking for highly intelligent individuals."

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
b'Hello. We are looking for highly intelligent individuals.'
```

---

# Features

- Symmetric key encryption
- Byte-oriented processing
- UTF-8 compatible through byte conversion
- Random cryptographic key generation
- Custom key encryption
- `.lemon` encrypted file format
- `.sourkey` key file format
- Lightweight Python API

---

# API Reference

## `encrypt()`

```python
encrypt(data_bytes: bytes) -> tuple[bytes, bytes]
```

Encrypts binary data and generates a random key with the same length as the input data.

### Arguments

| Argument | Type | Description |
|-|-|-|
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

| Argument | Type | Description |
|-|-|-|
| `data_bytes` | `bytes` | Data to encrypt |
| `key_bytes` | `bytes` | Existing encryption key |

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

### Arguments

| Argument | Type | Description |
|-|-|-|
| `crypt_bytes` | `bytes` | Encrypted data |
| `key_bytes` | `bytes` | Encryption key |

### Returns

The original data:

```python
bytes
```

Example:

```python
message = decrypt(crypt, key)
```

---

## `generate_key()`

```python
generate_key(length: int) -> bytes
```

Generates a cryptographically secure random key.

### Arguments

| Argument | Type | Description |
|-|-|-|
| `length` | `int` | Number of bytes |

### Returns

Generated key:

```python
bytes
```

---

# File Processing

Lemonade supports its own encrypted file formats.

## `.lemon`

Contains encrypted data.

Structure:

```
LEMON_MAGIC
encrypted bytes
```

## `.sourkey`

Contains encryption keys.

Structure:

```
SOURKEY_MAGIC
key bytes
```

A `.sourkey` file can be reused to encrypt multiple data sources.

Example:

```python
encrypt_with_sourkey_to_file(
    data,
    "output_directory",
    "key.sourkey"
)
```

---

# How It Works

Lemonade operates directly on byte values.

Example:

```
A = 65
B = 66
C = 67
```

The encryption operation is:

```
C = (M - K) mod 256
```

Where:

| Symbol | Meaning |
|-|-|
| `C` | Encrypted byte |
| `M` | Original data byte |
| `K` | Key byte |

The decryption operation reverses the transformation:

```
M = (C + K) mod 256
```

More technical details can be found in:

```
docs/algorithm.md
```

---

# Security Notice

Lemonade Cryptography is an experimental encryption library created for educational purposes and lightweight applications.

It is not intended to replace modern cryptographic standards such as AES or ChaCha20 in security-critical systems.

Always protect your encryption keys. Without the correct key, encrypted data cannot be recovered.

---

# License

Lemonade Cryptography is licensed under the MIT License.