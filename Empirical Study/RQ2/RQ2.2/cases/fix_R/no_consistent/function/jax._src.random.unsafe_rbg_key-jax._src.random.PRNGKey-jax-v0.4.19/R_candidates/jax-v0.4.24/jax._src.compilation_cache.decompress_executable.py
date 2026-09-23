def decompress_executable(executable):
  if zstandard:
    decompressor = zstandard.ZstdDecompressor()
    return decompressor.decompress(executable)
  else:
    return zlib.decompress(executable)
