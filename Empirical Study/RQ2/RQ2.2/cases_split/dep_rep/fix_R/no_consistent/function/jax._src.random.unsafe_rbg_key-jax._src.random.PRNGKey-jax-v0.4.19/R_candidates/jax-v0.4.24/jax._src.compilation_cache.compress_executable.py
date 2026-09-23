def compress_executable(executable):
  if zstandard:
    compressor = zstandard.ZstdCompressor()
    return compressor.compress(executable)
  else:
    return zlib.compress(executable)
