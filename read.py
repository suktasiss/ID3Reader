from collections import namedtuple
import math
import inspect

DEFAULT_ENCODING = 'UTF-8'
UTF16_ENCODING = 'UTF-16'
UTF16_SIZE_INT = 255

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
FRAME_PICTURE_TYPE_SIZE = 1
MIME_TYPE_END = 0
MAXIMUM_DESCRIPTION_SIZE = 64

# tag types
STRING_IDENTIFIER = 'T'
PICTURE_IDENTIFIER = 'A'

header_structure = namedtuple("header_structure", "marker version subversion flags size")
tag_structure = namedtuple("tag_structure", "id size flags encoding contents")
image_tag_structure = namedtuple("tag_structure", "id size flags encoding picture_type description contents")


def sync_safe_reader(numbers):
    """parse synchsafe integers"""
    k = ''
    if isinstance(numbers, bytes):
        numbers = int.from_bytes(numbers, byteorder='big')
    bits = "{0:08b}".format(numbers)
    bits = bits[::-1]
    slices = math.ceil(len(bits) / 8)
    bytess = []
    for i in range(slices):
        bytess.append(bits[i * 8:8*(i + 1)])
    for b in range(len(bytess)):
        k = k + bytess[len(bytess) - 1 - b][0:7]
    k = k[::-1]
    k = int(k, 2)
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
        identifier = tag_id[0]
        pointer = pointer + FRAME_TAG_SIZE
        size = contents[pointer:pointer + FRAME_SIZE_SIZE]
        size = sync_safe_reader(size)
        pointer = pointer + FRAME_SIZE_SIZE
        flags = int.from_bytes(contents[pointer:pointer+FRAME_FLAG_SIZE], 'big')
        pointer = pointer+FRAME_FLAG_SIZE
        encoding = contents[pointer + FRAME_ENC_SIZE]
        pointer = pointer + FRAME_ENC_SIZE

        # check encoding flag
        if encoding == UTF16_SIZE_INT:
            encoding_type = UTF16_ENCODING
        else :
            encoding_type = DEFAULT_ENCODING
        if identifier == PICTURE_IDENTIFIER:
            checkbytes = seek_string(contents[pointer:pointer+20])
            pointer = pointer + len(checkbytes) + 1
            picture_type = contents[pointer]
            pointer = pointer + FRAME_PICTURE_TYPE_SIZE
            description = seek_string(contents[pointer:pointer+MAXIMUM_DESCRIPTION_SIZE+1])
            pointer = pointer + len(description) + 1
            content = contents[pointer:pointer + size - 1]
            pointer = pointer + size + 1
        else: 
            content = contents[pointer:pointer + size - 1].decode(encoding_type)
            pointer = pointer + size - 1
            tag = tag_structure(tag_id, size, flags, encoding, content)
            tags.append(tag)
    return tags

def seek_string(seek_string):
    """read string till first \x00 occurence"""
    for i in range(len(seek_string)):
        if seek_string[i] == MIME_TYPE_END:
            return seek_string[:i].decode(DEFAULT_ENCODING)
    return 0

def print_tag(tag):
    """formatted tag structure output"""
    print(f'tag id: {tag.id}, size: {tag.size}, flags: {tag.flags}, contents: {tag.contents}')


def print_header(header):
    print(f'header marker: {header.marker}, version: {header.version}, '
          f'subversion: {header.subversion}, flags: {header.flags}, size: {header.size}')
