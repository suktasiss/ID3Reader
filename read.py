def sync_safe_reader(numbers):
    k = []
    for i in range(numbers.__len__()):
        formatted = format(numbers[i], 'b')
        if formatted.__len__() == 8:
            k.append(int(formatted[0:7]), 2)
        else:
            k.append(int(formatted, 2))
    k = int.from_bytes(bytes(k), byteorder='big')
    return k


with open('file.mp3', 'rb') as f:
    contents = f.read()
    marker = contents[:3]
    version = contents[3]
    subversion = contents[4]
    flags = contents[5]
    size = contents[6:10]
    print(f'\nmarker is {marker} \nversion is {version} \nsubversion is {subversion} '
          f'\nflags are {flags} \nlen is {sync_safe_reader(size)}')
