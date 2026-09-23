def vmap(
    func: Callable,
    in_dims: in_dims_t = 0,
    out_dims: out_dims_t = 0,
    randomness: str = "error",
    *,
    chunk_size=None,
) -> Callable:
    warn_deprecated("vmap", "torch.vmap")
    return apis.vmap(func, in_dims, out_dims, randomness, chunk_size=chunk_size)
