def compress_string(s):
    return gzip_compress(s, compresslevel=6, mtime=0)
