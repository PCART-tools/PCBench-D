  def put(self, key: str, value: bytes):
    """Adds new cache entry."""
    if not key:
      raise ValueError("key cannot be empty")
    path_to_new_file = self._path / key
    if str(path_to_new_file).startswith('gs://'):
      # Writes to gcs are atomic.
      path_to_new_file.write_bytes(value)
    elif str(path_to_new_file).startswith('file://') or '://' not in str(path_to_new_file):
      tmp_path = self._path / f"_temp_{key}"
      with open(str(tmp_path), "wb") as f:
        f.write(value)
        f.flush()
        os.fsync(f.fileno())
      os.replace(tmp_path, path_to_new_file)
    else:
      tmp_path = self._path / f"_temp_{key}"
      tmp_path.write_bytes(value)
      tmp_path.replace(str(path_to_new_file))
