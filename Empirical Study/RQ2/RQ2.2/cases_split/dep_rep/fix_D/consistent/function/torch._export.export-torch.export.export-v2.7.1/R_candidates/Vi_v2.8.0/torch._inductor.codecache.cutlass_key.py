@torch_key_cache
def cutlass_key() -> bytes:
    """
    Compute a key representing the state of the CUTLASS library.

    Note: OSS and fbcode will have different keys.
    """
    if config.is_fbcode():
        with importlib.resources.path("cutlass", "src_hash.txt") as resource_path:
            with open(resource_path) as resource_file:
                return resource_file.read().encode()

    combined_hash = hashlib.sha256()
    build_code_hash([config.cuda.cutlass_dir], "", combined_hash)
    return combined_hash.digest()
