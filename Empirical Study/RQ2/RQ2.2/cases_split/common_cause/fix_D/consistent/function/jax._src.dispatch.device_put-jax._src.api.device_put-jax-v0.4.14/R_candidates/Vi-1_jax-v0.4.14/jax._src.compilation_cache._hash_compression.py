def _hash_compression(hash_obj):
  _hash_string(hash_obj, "zstandard" if zstandard is not None else "zlib")
