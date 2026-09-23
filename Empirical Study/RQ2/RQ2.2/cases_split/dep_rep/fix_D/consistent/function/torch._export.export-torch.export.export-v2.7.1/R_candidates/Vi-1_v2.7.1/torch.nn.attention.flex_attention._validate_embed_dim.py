def _validate_embed_dim(query: Tensor, key: Tensor, value: Tensor):
    if query.size(-1) != key.size(-1):
        raise ValueError(
            f"Expect query and key/value to have the same embedding dimension "
            f"but got E={query.size(-1)} and E={key.size(-1)}."
        )
    return
    # TODO this config segfaults with Triton without:
    # https://github.com/triton-lang/triton/pull/4540
    if not (
        _supported_head_dim(query.size(-1)) and _supported_head_dim(value.size(-1))
    ):
        raise ValueError(
            f"NYI: Currently non power of 2 embedding dimension are not supported. "
            f"Got E={query.size(-1)} and Ev={value.size(-1)}."
        )
