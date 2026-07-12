# Changelog

## 1.1.0 (07/12/2026)

Features:
- Added `.lemon` file processing
- Added `.sourkey` file processing
- Added encryption using existing `.sourkey` files
- Added byte-based encryption support
- Added support for custom encryption keys

Improvements:
- Refactored encryption core to operate directly on bytes
- Separated key generation into its own function
- Improved internal encryption architecture

---

## 1.0.0 (07/09/2026)

Initial release.

Features:
- Basic encryption
- Decryption
- UTF-8 support
- Base64 output