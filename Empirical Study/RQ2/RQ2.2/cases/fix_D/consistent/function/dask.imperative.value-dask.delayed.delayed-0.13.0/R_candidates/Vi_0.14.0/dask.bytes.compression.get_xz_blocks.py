def get_xz_blocks(fp):
    from lzmaffi import (STREAM_HEADER_SIZE, decode_stream_footer,
                         decode_index, LZMAError)
    fp.seek(0, 2)

    def _peek(f, size):
        data = f.read(size)
        f.seek(-size, 1)
        return data

    if fp.tell() < 2 * STREAM_HEADER_SIZE:
        raise LZMAError("file too small")

    # read stream paddings (4 bytes each)
    fp.seek(-4, 1)
    padding = 0
    while _peek(fp, 4) == b'\x00\x00\x00\x00':
        fp.seek(-4, 1)
        padding += 4

    fp.seek(-STREAM_HEADER_SIZE + 4, 1)

    stream_flags = decode_stream_footer(_peek(fp, STREAM_HEADER_SIZE))
    fp.seek(-stream_flags.backward_size, 1)

    index = decode_index(_peek(fp, stream_flags.backward_size), padding)
    return {'offsets': [b.compressed_file_offset for i, b in index],
            'lengths': [b.unpadded_size for i, b in index],
            'check': stream_flags.check}
