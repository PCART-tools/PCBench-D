def file_to_blocks(lazy_file):
    with lazy_file as f:
        for line in f:
            yield line
