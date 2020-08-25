import read
import sys

if len(sys.argv) == 1:
    print('add file name as argument')
    sys.exit()

file_name = str(sys.argv[1])

with open(file_name, 'rb') as f:

    contents = f.read()

    # header parsing
    header = read.read_header(contents)

    tags = contents[read.TAGS_INDEX_START:header.size + read.HEADER_SIZE]

    # tag parsing
    tags = read.read_tags(tags)