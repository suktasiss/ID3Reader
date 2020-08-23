from collections import namedtuple

DEFAULT_ENCODING = 'UTF-8'

# header constants
INDEX_MARKER_END = 3
INDEX_VERSION = 3
INDEX_SUBVERSION = 4
INDEX_FLAGS = 5
INDEX_SIZE_START = 6
INDEX_SIZE_END = 10
TAGS_INDEX_START = 10
HEADER_SIZE = 10

# frame constants
FRAME_TAG_SIZE = 4
FRAME_SIZE_SIZE = 4
FRAME_FLAG_SIZE = 2
FRAME_ENC_SIZE = 1

header_structure = namedtuple("header_structure", "marker version subversion flags size")
tag_structure = namedtuple("tag_structure", "id size flags encoding contents")


def sync_safe_reader(numbers):
    """parse synchsafe integers"""
    k = []
    for i in range(numbers.__len__()):
        formatted = format(numbers[i], 'b')
        if formatted.__len__() == 8:
            k.append(int(formatted[0:7]), 2)
        else:
            k.append(int(formatted, 2))
    k = int.from_bytes(bytes(k), byteorder='big')
    return k


def read_header(contents):
    """parse ID3 Header"""
    marker = contents[:INDEX_MARKER_END]
    version = contents[INDEX_VERSION]
    subversion = contents[INDEX_SUBVERSION]
    flags = contents[INDEX_FLAGS]
    size = sync_safe_reader(contents[INDEX_SIZE_START:INDEX_SIZE_END])
    header = header_structure(marker, version, subversion, flags, size)
    return header


def read_tags(contents):
    """parse tags and return array of tag structures"""
    pointer = 0
    tags = []
    while pointer < len(contents):
        tag_id = contents[pointer:pointer + FRAME_TAG_SIZE].decode(DEFAULT_ENCODING)
        pointer = pointer + FRAME_TAG_SIZE
        size = contents[pointer:pointer + FRAME_SIZE_SIZE]
        size = sync_safe_reader(size)
        pointer = pointer + FRAME_SIZE_SIZE
        flags = int.from_bytes(contents[pointer:pointer+FRAME_FLAG_SIZE], 'big')
        pointer = pointer+FRAME_FLAG_SIZE
        encoding = contents[pointer + FRAME_ENC_SIZE]
        pointer = pointer + FRAME_ENC_SIZE
        content = contents[pointer:pointer + size - 1].decode(DEFAULT_ENCODING)
        pointer = pointer + size - 1
        tag = tag_structure(tag_id, size, flags, encoding, content)
        tags.append(tag)
    return tags


def print_tag(tag):
    """formatted tag structure output"""
    print(f'tag id: {tag.id}, size: {tag.size}, flags: {tag.flags}, contents: {tag.contents}')


def print_header(header):
    print(f'header marker: {header.marker}, version: {header.version}, '
          f'subversion: {header.subversion}, flags: {header.flags}, size: {header.size}')
