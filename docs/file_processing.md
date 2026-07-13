# 🍋 Lemonade File Processing

## Overview

Lemonade Cryptography provides a custom binary file processing system designed to store encrypted data and encryption keys separately.

The system uses two file formats:

* `.lemon` — encrypted data container
* `.sourkey` — encryption key storage

The separation between encrypted data and keys allows users to store and manage encryption keys independently from encrypted files.

A complete encrypted file operation uses:

```
Original File
      |
      v
Encryption
      |
      +----------------+
      |                |
      v                v
.lemon File      .sourkey File
(Encrypted Data) (Encryption Key)
```

---

# `.lemon` File Format

## Purpose

A `.lemon` file is the main encrypted data container.

It stores:

* File format identification
* Version information
* Metadata
* Encrypted binary data

The `.lemon` file does not contain the encryption key.

The key must be provided separately through a `.sourkey` file.

---

# `.lemon` Structure

The binary structure is:

```
+----------------+
|  LEMON_MAGIC   |
+----------------+
|    VERSION     |
+----------------+
| METADATA SIZE  |
+----------------+
|    METADATA    |
+----------------+
| ENCRYPTED DATA |
+----------------+
```

---

# LEMON_MAGIC

The first bytes of every `.lemon` file contain a fixed identifier:

```
LEMON_MAGIC
```

Current value:

```
🍋🔒
```

Binary representation:

```
F0 9F 8D 8B F0 9F 94 92
```

The magic bytes allow Lemonade to identify whether a file is a valid `.lemon` file.

During decryption:

1. The first bytes are read.
2. They are compared with `LEMON_MAGIC`.
3. If they do not match, an invalid file error is raised.

Example:

```
Invalid file:

12 FF 40 99 ...


Expected:

F0 9F 8D 8B F0 9F 94 92
```

---

# Version Section

After the magic bytes, the file stores the Lemonade version used to create the file.

Structure:

```
VERSION_LENGTH
VERSION_DATA
```

Example:

```
02
31 2E 32
```

Meaning:

```
Version:
1.2
```

The version system allows future versions of Lemonade to introduce changes while maintaining compatibility checks.

During decryption:

1. The version length is read.
2. The version is extracted.
3. The version is compared against supported versions.
4. Unsupported versions are rejected.

---

# Metadata Section

Metadata stores information about the original file.

Structure:

```
METADATA_SIZE
METADATA_DATA
```

The metadata section uses a field-based binary format.

Each field follows:

```
+------------+
| IDENTIFIER |
+------------+
| DATA SIZE  |
+------------+
| DATA       |
+------------+
```

Where:

| Field      | Size     |
| ---------- | -------- |
| Identifier | 1 byte   |
| Data size  | 4 bytes  |
| Data       | Variable |

---

# Metadata Fields

Current metadata fields:

| Identifier | Description                 |
| ---------- | --------------------------- |
| FILENAME   | Original filename           |
| EXTENSION  | Original file extension     |
| SIZE       | Original file size          |
| TIMESTAMP  | Last modification timestamp |
| SHA256     | Integrity verification hash |

---

## FILENAME

Stores the original filename.

Example:

```
hello.txt
```

Used during decryption to recreate the original file name.

---

## EXTENSION

Stores the original file extension.

Example:

```
.txt
```

Allows applications to identify the original file type.

---

## SIZE

Stores the original file size.

The value is stored as an unsigned 64-bit integer.

Example:

```
1024 bytes
```

---

## TIMESTAMP

Stores the original modification timestamp.

The value is stored as a floating-point timestamp.

Example:

```
1760000000.123
```

---

## SHA256

Stores the SHA-256 hash of the original file data.

Purpose:

* Detect corrupted encrypted files
* Detect invalid decryption keys
* Verify restored data integrity

During decryption:

```
Decrypted Data
      |
      v
Calculate SHA-256
      |
      v
Compare with Metadata Hash
```

If hashes do not match:

```
IntegrityError
```

is raised.

---

# Encrypted Data Section

The final section contains the encrypted bytes.

Structure:

```
ENCRYPTED_DATA
```

The data is generated using the Lemonade encryption algorithm:

```
C = (M - K) mod 256
```

Where:

| Symbol | Meaning        |
| ------ | -------------- |
| C      | Encrypted byte |
| M      | Original byte  |
| K      | Key byte       |

The encrypted data cannot be restored without the correct `.sourkey`.

---

# `.sourkey` File Format

## Purpose

A `.sourkey` file stores encryption keys separately from encrypted data.

Separating keys from encrypted files provides:

* Independent key management
* Key reuse
* Easier storage and transfer

---

# `.sourkey` Structure

The binary structure is:

```
+---------------+
| SOURKEY_MAGIC |
+---------------+
|   KEY BYTES   |
+---------------+
```

---

# SOURKEY_MAGIC

The first bytes identify the file as a Lemonade key file.

Current value:

```
🍋🔑
```

Binary representation:

```
F0 9F 8D 8B F0 9F 94 91
```

During key loading:

1. Magic bytes are checked.
2. Invalid files are rejected.

---

# Key Section

After the magic bytes, the remaining data represents the encryption key.

Example:

```
SOURKEY_MAGIC

23 190 51 8 200 ...
```

The key length is determined by the remaining file size.

---

# Encryption Workflow

## Automatic Key Generation

When using:

```python
encrypt_to_file()
```

The process is:

```
Original File
      |
      v
Read Bytes
      |
      v
Generate Random Key
      |
      +----------------+
      |                |
      v                v
Encrypt Data      Save Key
      |                |
      v                v
.lemon File      .sourkey File
```

---

# Existing Key Workflow

When using:

```python
encrypt_with_sourkey_to_file()
```

The process is:

```
Original File
      |
      v
Read Existing .sourkey
      |
      v
Encrypt Data
      |
      v
Create .lemon File
```

The original `.sourkey` remains unchanged.

---

# Decryption Workflow

When using:

```python
decrypt_from_file()
```

The process is:

```
.lemon File
      |
      v
Read Metadata
      |
      v
Read Encrypted Bytes


.sourkey File
      |
      v
Read Encryption Key


Encrypted Bytes + Key
      |
      v
Decrypt
      |
      v
Verify SHA256
      |
      v
Restore Original File
```

---

# File Security Model

Lemonade separates:

```
Encrypted Data
+
Encryption Key
```

A `.lemon` file alone is insufficient to recover the original data.

A `.sourkey` file alone contains no encrypted content.

Both are required:

```
.lemon + .sourkey
        |
        v
Original File
```

---

# Compatibility

`.lemon` files contain version information to allow future format changes.

When a file is opened:

1. Magic bytes are verified.
2. Version compatibility is checked.
3. Metadata is parsed.
4. Data is decrypted.

Unsupported formats are rejected instead of being processed incorrectly.

---

# Summary

Lemonade file processing uses two custom binary formats:

## `.lemon`

Contains:

* File identification
* Version
* Metadata
* Encrypted data

## `.sourkey`

Contains:

* File identification
* Encryption key

Together they provide a complete encrypted file storage system with:

* Binary file support
* Metadata preservation
* SHA-256 integrity verification
* Separate key management
* Version-aware processing
