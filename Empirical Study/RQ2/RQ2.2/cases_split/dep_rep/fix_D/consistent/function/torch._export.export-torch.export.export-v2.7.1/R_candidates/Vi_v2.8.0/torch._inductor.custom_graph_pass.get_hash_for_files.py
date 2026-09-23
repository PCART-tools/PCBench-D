@lru_cache(1)
def get_hash_for_files(paths: tuple[str], extra: str = "") -> bytes:
    """
    Helper to compute a unique string by hashing the contents of a list of files.
    """
    hasher = hashlib.sha256()
    hasher.update(extra.encode("utf-8"))
    for path in paths:
        with open(path, "rb") as f:
            hasher.update(path.encode("utf-8"))
            hasher.update(f.read())
    return hasher.digest()
