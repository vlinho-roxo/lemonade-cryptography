# 🍋 Lemonade Cryptography Algorithm

## Overview

Lemonade Cryptography is a symmetric byte-oriented encryption algorithm based on modular arithmetic.

The algorithm operates directly on binary data by applying mathematical transformations between data bytes and secret key bytes.

The encryption process uses subtraction:

```
Encrypted Byte = (Data Byte - Key Byte) mod 256
```

The decryption process performs the inverse operation:

```
Data Byte = (Encrypted Byte + Key Byte) mod 256
```

Because addition and subtraction are inverse operations under modulo 256 arithmetic, the original data can be restored using the same key.

---

# Byte Representation

Computers store information as numerical byte values.

Example:

```
A = 65
B = 66
C = 67
```

Lemonade does not encrypt characters directly. It processes raw bytes.

Example:

```
Data:

ABC


Bytes:

65 66 67
```

Because the algorithm operates on bytes, it can process any binary data, including:

- Text
- Images
- Audio
- Videos
- Other binary files

---

# Key Generation

Lemonade generates cryptographic keys using Python's secure random generator:

```python
secrets.token_bytes(length)
```

The generated key consists of random bytes.

Example:

```
Data bytes:

72 101 108 108 111


Generated key:

23 190 51 8 200
```

Each byte of the data is combined with a corresponding key byte.

---

# Encryption Process

The main encryption formula is:

```
C = (M - K) mod 256
```

Where:

| Symbol | Meaning |
|-|-|
| `C` | Ciphertext byte |
| `M` | Data byte |
| `K` | Key byte |

Example:

```
Data byte:

72


Key byte:

23


Calculation:

72 - 23 = 49


Encrypted byte:

49
```

If subtraction generates a negative value:

```
101 - 190 = -89
```

Modulo 256 keeps the result inside the valid byte range:

```
-89 mod 256 = 167
```

---

# Key Repetition

Lemonade supports encryption using existing keys.

When the provided key is smaller than the data, the key is repeated cyclically.

Example:

```
Data:

ABCDEFG


Key:

XYZ
```

The key is reused:

```
Used key:

XYZXYZX
```

The encryption continues normally:

```
C = (M - K) mod 256
```

This allows `.sourkey` files to be reused for different encryption operations.

---

# Decryption Process

The reverse operation is applied:

```
M = (C + K) mod 256
```

Example:

```
Encrypted byte:

49


Key byte:

23


Calculation:

49 + 23 = 72


Original byte:

72
```

The process is repeated until all encrypted bytes are restored.

---

# File Formats

Lemonade provides custom binary file formats for encrypted data and keys.

---

# `.lemon` Format

A `.lemon` file stores encrypted data.

Structure:

```
LEMON_MAGIC
Encrypted Bytes
```

The `LEMON_MAGIC` sequence identifies the file as a valid Lemonade encrypted file.

---

# `.sourkey` Format

A `.sourkey` file stores encryption keys.

Structure:

```
SOURKEY_MAGIC
Key Bytes
```

The `SOURKEY_MAGIC` sequence identifies the file as a valid Lemonade key file.

A `.sourkey` file can be reused to encrypt multiple pieces of data.

---

# Data Flow

The complete encryption process:

```
Input Data
    |
    v
Bytes
    |
    +---- Encryption Key
    |
    v
Modulo 256 Transformation
    |
    v
Encrypted Bytes
    |
    +---- LEMON_MAGIC
    |
    v
.lemon File
```

Key generation:

```
Random Length
    |
    v
Secure Random Bytes
    |
    +---- SOURKEY_MAGIC
    |
    v
.sourkey File
```

---

# Technical Properties

## Encryption Type

```
Symmetric encryption
```

The same secret key is required for encryption and decryption.

---

## Processing Model

```
Byte-oriented transformation
```

Each byte is processed independently.

---

## Arithmetic

```
Modulo 256
```

All results remain valid byte values:

```
0 <= byte <= 255
```

---

## Complexity

For data containing `n` bytes:

### Encryption

```
Time Complexity: O(n)
```

### Decryption

```
Time Complexity: O(n)
```

Memory usage:

```
O(n)
```

---

# Base64 Representation

Previous versions of Lemonade used Base64 encoding to represent encrypted data as text.

Version 1.1.0 works directly with bytes.

Base64 may still be used by applications when text representation is required, but it is not part of the core encryption algorithm.

Base64 does not provide encryption. It only represents binary data as text.

---

# Limitations

Lemonade Cryptography is a custom encryption algorithm designed for educational purposes.

It should not be considered a replacement for professionally analyzed cryptographic standards.

Security depends heavily on:

- Keeping the key secret
- Using strong and appropriate keys
- Never losing the key
- Using the encryption process correctly

---

# Summary

Lemonade Cryptography is a lightweight symmetric byte-based encryption system that uses:

- Direct byte processing
- Secure random key generation
- Modular subtraction for encryption
- Modular addition for decryption
- Custom `.lemon` encrypted files
- Custom `.sourkey` key files
- Optional reusable keys

It provides a simple way to understand the fundamentals of key-based cryptographic transformations while supporting arbitrary binary data.