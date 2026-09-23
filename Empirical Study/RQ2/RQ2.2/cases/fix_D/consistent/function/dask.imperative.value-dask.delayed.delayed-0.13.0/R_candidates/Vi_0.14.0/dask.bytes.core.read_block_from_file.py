def read_block_from_file(lazy_file, off, bs, delimiter):
    with lazy_file as f:
        return read_block(f, off, bs, delimiter)
