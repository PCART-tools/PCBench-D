def extract_executable_and_time(
    exectuable_and_time: bytes
) -> tuple[bytes, int]:
  """Given the cache entry in the format shown below, extract the serialized
  executable and the compilation time.

  The cache entry 'executable_and_time' is of the form:
  Byte:     0    1    2    3    4 ...
  Content:  compilation time    serialized executable
            (big-endian int)
  """
  return exectuable_and_time[4:], int.from_bytes(
      exectuable_and_time[:4], byteorder='big')
