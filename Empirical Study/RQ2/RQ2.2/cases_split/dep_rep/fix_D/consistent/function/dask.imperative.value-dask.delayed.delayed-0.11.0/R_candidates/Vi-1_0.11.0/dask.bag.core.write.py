def write(data, filename, compression, encoding):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        with ignoring(OSError):
            os.makedirs(dirname)

    f = open(filename, mode='wb', compression=compression)

    # Check presence of endlines
    data = iter(data)
    try:
        firstline = next(data)
    except StopIteration:
        f.close()
        return
    if not (firstline.endswith(os.linesep) or firstline.endswith('\n')):
        sep = os.linesep if firstline.endswith(os.linesep) else '\n'
        firstline = firstline + sep
        data = (line + sep for line in data)
    f.write(firstline.encode(encoding))

    try:
        lastline = ''
        for line in data:
            f.write(lastline.encode(encoding))
            lastline = line
        f.write(lastline.rstrip(os.linesep).encode(encoding))

    finally:
        f.close()
