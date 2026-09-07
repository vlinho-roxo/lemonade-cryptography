# Changelog

## 1.2.1 Minor bug fix - (07/13/2026)

Fix:

* Decrypt function couldn't decrypt with keys shorter than cipher 

## 1.2.0 File Format Evolution - (07/13/2026)

Features:

* Added complete file encryption and decryption support
* Added `.lemon` file format with versioning support
* Added `.sourkey` file format for separated encryption keys
* Added file metadata storage
* Added automatic filename restoration after decryption
* Added SHA-256 integrity verification
* Added integrity error detection for corrupted or invalid files
* Added support for decrypting files directly into an output directory

Metadata:

* Added filename metadata
* Added file extension metadata
* Added file size metadata
* Added file timestamp metadata
* Added SHA-256 hash metadata

Improvements:

* Refactored file encryption architecture
* Improved binary file handling using byte-based operations
* Added file format validation through magic headers
* Added version compatibility validation
* Improved error handling for invalid `.lemon` and `.sourkey` files

---

## 1.1.0 File processing - (07/12/2026)

Features:

* Added `.lemon` file processing
* Added `.sourkey` file processing
* Added encryption using existing `.sourkey` files
* Added byte-based encryption support
* Added support for custom encryption keys

Improvements:

* Refactored encryption core to operate directly on bytes
* Separated key generation into its own function
* Improved internal encryption architecture

---

## 1.0.0 The Lemonade Cryptography - (07/09/2026)

Initial release.

Features:

* Basic encryption
* Decryption
* UTF-8 support
* Base64 output
