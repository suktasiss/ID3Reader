import read

INDEX_MARKER_END = 3
INDEX_VERSION = 3
INDEX_SUBVERSION = 4
INDEX_FLAGS = 5
INDEX_SIZE_START = 6
INDEX_SIZE_END = 10
TAGS_INDEX_START = 11
HEADER_SIZE = 10

with open('file.mp3', 'rb') as f:
    contents = f.read()
    marker = contents[:INDEX_MARKER_END]
    version = contents[INDEX_VERSION]
    subversion = contents[INDEX_SUBVERSION]
    flags = contents[INDEX_FLAGS]
    size = read.sync_safe_reader(contents[INDEX_SIZE_START:INDEX_SIZE_END])
    print(f'\nmarker is {marker} \nversion is {version} \nsubversion is {subversion} '
          f'\nflags are {flags} \nlen is {size}')
    tags = contents[TAGS_INDEX_START:size + HEADER_SIZE]
