# 🍋 Lemonade Cryptography Algorithm

## Overview

Lemonade Cryptography is a symmetric byte-oriented encryption algorithm based on modular arithmetic.

The algorithm converts a plaintext message into bytes and combines each byte with a randomly generated secret key.

The encryption process uses subtraction:

```
Encrypted Byte = (Message Byte - Key Byte) mod 256
```

The decryption process performs the inverse operation:

```
Message Byte = (Encrypted Byte + Key Byte) mod 256
```

Because addition and subtraction are inverse operations under modulo 256 arithmetic, the original message can be restored using the same key.

---

# Byte Representation

Computers store text as numerical byte values.

Example:

```
A = 65
B = 66
C = 67
```

Before encryption, Lemonade converts the message into UTF-8 bytes:

```python
message.encode("utf-8")
```

Example:

```
Message:

ABC


Bytes:

65 66 67
```

---

# Key Generation

Lemonade generates a random key using Python's secure random generator:

```python
secrets.token_bytes(length)
```

The key length is equal to the message length in bytes.

Example:

```
Message bytes:

72 101 108 108 111


Generated key:

23 190 51 8 200
```

Each message byte has a corresponding key byte.

---

# Encryption Process

The encryption formula is:

```
C = (M - K) mod 256
```

Where:

| Symbol | Meaning |
|-|-|
| `C` | Ciphertext byte |
| `M` | Message byte |
| `K` | Key byte |

Example:

```
Message byte:

72


Key byte:

23


Calculation:

72 - 23 = 49


Encrypted byte:

49
```

If the result becomes negative:

```
101 - 190 = -89
```

Modulo 256 keeps the value inside the byte range:

```
-89 mod 256 = 167
```

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

72 = H
```

This process is repeated for every byte.

---

# Base64 Encoding

Encrypted bytes may contain values that cannot be represented as readable text.

For storage and transmission, Lemonade converts the binary data into Base64.

Example:

```
Encrypted bytes:

10101100 00101101 11100010


Base64:

rC3i
```

Base64 does not provide encryption. It only represents binary data as text.

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

## Character Encoding

Lemonade uses UTF-8:

```python
msg.encode("utf-8")
```

Supported content includes:

- English characters
- Latin characters
- Symbols
- Emojis
- Unicode characters

---

# Complexity

For a message containing `n` bytes:

## Encryption

```
Time Complexity: O(n)
```

## Decryption

```
Time Complexity: O(n)
```

Memory usage:

```
O(n)
```

---

# Data Flow

The complete encryption process:

```
Plaintext
    |
    v
UTF-8 Encoding
    |
    v
Message Bytes
    |
    +---- Secret Key
    |
    v
Modulo 256 Transformation
    |
    v
Encrypted Bytes
    |
    v
Base64 Encoding
    |
    v
Encrypted String
```

---

# Limitations

Lemonade Cryptography is a custom encryption algorithm designed for educational purposes.

It should not be considered a replacement for professionally analyzed cryptographic standards.

Security depends heavily on:

- Keeping the key secret
- Never losing the key
- Using the encryption process correctly

---

# Summary

Lemonade Cryptography is a lightweight symmetric byte-based encryption system that uses:

- UTF-8 byte conversion
- Random key generation
- Modular subtraction for encryption
- Modular addition for decryption
- Base64 encoding for representation

It provides a simple way to understand the fundamentals of key-based cryptographic transformations.