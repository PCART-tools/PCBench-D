def get_hash(
    content: Union[str, bytes], extra: str = "", hash_type: str = "code"
) -> str:
    if hash_type == "code":
        return code_hash(content, extra)
    if hash_type in ["cubin", "hsaco", "spv"]:
        return code_hash(repr(content))
    raise AssertionError(f"Unknown hash type {hash_type}")
