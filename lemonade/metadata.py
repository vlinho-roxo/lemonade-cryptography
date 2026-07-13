import os
import struct

from dataclasses import dataclass
from .metadata_type import MetadataType

@dataclass
class MetadataField:
    identifier: MetadataType
    data: bytes
    
    def encode(self) -> bytes:
        return (
            self.identifier.value.to_bytes(1, "big") +
            len(self.data).to_bytes(4, "big") +
            self.data
        )

def generate_metadata_bytes(
    filePath: str
) -> bytes:
    """
    Generates binary metadata from a file.

    The metadata stores information about the original file,
    including:

        - Filename
        - File extension
        - File size
        - Last modification timestamp

    Metadata format:

        [IDENTIFIER][DATA LENGTH][DATA]

    Where:

        IDENTIFIER:
            1 byte representing the MetadataType.

        DATA LENGTH:
            4 bytes representing the size of the stored data.

        DATA:
            Raw metadata bytes.

    Args:
        filePath (str):
            Path to the original file.

    Returns:
        bytes:
            Serialized metadata in binary format.

    Raises:
        OSError:
            When the file path is invalid or inaccessible.
    """
    
    filename = os.path.basename(filePath)
    extension = os.path.splitext(filename)[1]
    file_size = os.path.getsize(filePath)
    timestamp = os.path.getmtime(filePath)
    
    filename_bytes = filename.encode("utf-8")
    extension_bytes = extension.encode("utf-8")
    size_bytes = struct.pack(
        "Q",
        file_size
    )
    timestamp_bytes = struct.pack(
        "d",
        timestamp
    )
    
    fields = [
        MetadataField(
            MetadataType.FILENAME,
            filename_bytes
        ),
        MetadataField(
            MetadataType.EXTENSION,
            extension_bytes
        ),
        MetadataField(
            MetadataType.SIZE,
            size_bytes
        ),
        MetadataField(
            MetadataType.TIMESTAMP,
            timestamp_bytes
        )
    ]

    metadata = b""

    for field in fields:
        metadata += field.encode()

    return metadata


def read_metadata(
    metadata_bytes: bytes
) -> list[MetadataField]:
    """
    Reads binary metadata and converts it into MetadataField objects.

    Args:
        metadata_bytes (bytes):
            Binary metadata.

    Returns:
        list[MetadataField]:
            Metadata fields extracted from metadata.
    """

    fields = []

    offset = 0

    while offset < len(metadata_bytes):

        identifier = MetadataType(
            metadata_bytes[offset]
        )

        offset += 1

        data_size = int.from_bytes(
            metadata_bytes[offset:offset + 4],
            "big"
        )

        offset += 4

        data = metadata_bytes[
            offset:offset + data_size
        ]

        offset += data_size

        fields.append(
            MetadataField(
                identifier,
                data
            )
        )

    return fields