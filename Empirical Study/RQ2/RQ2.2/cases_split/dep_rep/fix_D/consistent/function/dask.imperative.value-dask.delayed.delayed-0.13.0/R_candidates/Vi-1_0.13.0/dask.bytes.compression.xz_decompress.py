def xz_decompress(data, check):
    from lzmaffi import decode_block_header_size, LZMADecompressor, FORMAT_BLOCK
    hsize = decode_block_header_size(data[:1])
    header = data[:hsize]
    dc = LZMADecompressor(format=FORMAT_BLOCK, header=header,
                          unpadded_size=len(data), check=check)
    return dc.decompress(data[len(header):])
