import read

with open('file.mp3', 'rb') as f:

    contents = f.read()

    # header parsing
    header = read.read_header(contents)

    tags = contents[read.TAGS_INDEX_START:header.size + read.HEADER_SIZE]

    # tag parsing
    tags = read.read_tags(tags)
