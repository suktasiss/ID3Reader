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
