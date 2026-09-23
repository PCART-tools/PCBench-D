def get_config_request_key(
    arch: str,
    cuda_version: str,
    instantiation_level: str,
) -> str:
    """
    Return a key for the full ops, based on cutlass key, arch, cuda version, and instantiation level.
    """
    hash_target = "-".join(
        [
            cutlass_key().hex(),
            arch,
            cuda_version,
            instantiation_level,
        ]
    )
    return hashlib.sha256(hash_target.encode("utf-8")).hexdigest()[0:8]
