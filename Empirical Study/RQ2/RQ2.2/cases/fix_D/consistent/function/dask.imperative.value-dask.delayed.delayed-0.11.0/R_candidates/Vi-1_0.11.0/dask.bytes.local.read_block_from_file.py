def read_block_from_file(path, offset, length, delimiter, compression):
    with open(path, 'rb') as f:
        if compression:
            f = SeekableFile(f)
            f = compress_files[compression](f)
        try:
            result = read_block(f, offset, length, delimiter)
        finally:
            f.close()
    return result
