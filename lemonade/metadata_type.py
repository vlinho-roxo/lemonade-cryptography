import enum

class MetadataType(enum.Enum):
    FILENAME  = 1
    EXTENSION = 2
    SIZE      = 3
    TIMESTAMP = 4
    SHA256    = 5