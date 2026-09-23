def max_memory_cached(device: Union[Device, int] = None) -> int:
    r"""Deprecated; see :func:`~torch.cuda.max_memory_reserved`."""
    warnings.warn(
        "torch.cuda.max_memory_cached has been renamed to torch.cuda.max_memory_reserved",
        FutureWarning)
    return max_memory_reserved(device=device)
