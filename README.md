# 🍋 Lemonade Cryptography

**Lemonade Cryptography** is a lightweight byte-oriented encryption library based on modular arithmetic and symmetric key transformations.

Lemonade transforms readable messages into encrypted data by converting text into bytes and applying mathematical operations using a cryptographic key.

The core concept is:

> Each byte of the message is encrypted by subtracting it from a corresponding byte of a secret key.

The original message can be recovered by applying the reverse operation using the same key.

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

message = "Hello. We are looking for highly intelligent individuals."

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
<encrypted data>

Key:
<secret key>

Decrypted:
Hello. We are looking for highly intelligent individuals.
```

---

# Features

- Symmetric key encryption
- Byte-oriented processing
- UTF-8 message support
- Random cryptographic key generation
- Base64 encoded output
- Simple Python API
- Lightweight implementation

---

# API Reference

## `encrypt()`

```python
encrypt(msg: str) -> tuple[str, str]
```

Encrypts a message and generates a random key.

### Arguments

| Argument | Type | Description |
|-|-|-|
| `msg` | `str` | Message to encrypt |

### Returns

A tuple containing:

```python
(
    encrypted_message,
    encryption_key
)
```

Both values are encoded using Base64.

Example:

```python
crypt, key = encrypt("Hello")
```

---

## `decrypt()`

```python
decrypt(crypt: str, key: str) -> str
```

Decrypts a Lemonade encrypted message using its key.

### Arguments

| Argument | Type | Description |
|-|-|-|
| `crypt` | `str` | Encrypted message in Base64 |
| `key` | `str` | Encryption key in Base64 |

### Returns

The original message:

```python
str
```

Example:

```python
message = decrypt(crypt, key)
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
| `M` | Original message byte |
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

Always protect your encryption keys. Without the correct key, encrypted messages cannot be recovered.

---

# License

Lemonade Cryptography is licensed under the MIT License.