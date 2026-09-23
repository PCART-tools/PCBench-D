def file_size(fn, compression=None):
    """ Size of a file on disk

    If compressed then return the uncompressed file size
    """
    if compression == 'gzip':
        with open(fn, 'rb') as f:
            f.seek(-4, 2)
            result = struct.unpack('I', f.read(4))[0]
    elif compression:
        # depending on the implementation, this may be inefficient
        with open(fn, 'rb', compression) as f:
            result = f.seek(0, 2)
    else:
        result = os.stat(fn).st_size
    return result
