from .version import __version__

LEMON_MAGIC = b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x92"
SOURKEY_MAGIC = b"\xF0\x9F\x8D\x8B\xF0\x9F\x94\x91"

VERSION = __version__.encode("utf-8")

SUPPORTED_VERSIONS = [VERSION]

CHUNK_SIZE = 1024 * 1024