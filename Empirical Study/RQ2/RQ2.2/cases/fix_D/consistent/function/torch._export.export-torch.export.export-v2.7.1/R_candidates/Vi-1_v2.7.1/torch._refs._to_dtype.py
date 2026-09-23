@_to_dispatch.register
def _to_dtype(
    dtype: torch.dtype,
    non_blocking: bool = False,
    copy: bool = False,
    memory_format: Optional[torch.memory_format] = None,
) -> dict[str, Any]:
    kwargs = {
        "dtype": dtype,
        "non_blocking": non_blocking,
        "copy": copy,
        "memory_format": memory_format,
    }
    return kwargs
