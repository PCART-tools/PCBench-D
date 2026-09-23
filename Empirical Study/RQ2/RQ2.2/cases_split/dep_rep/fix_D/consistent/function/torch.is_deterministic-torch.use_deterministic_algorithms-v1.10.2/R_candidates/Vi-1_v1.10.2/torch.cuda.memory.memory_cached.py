def memory_cached(device: Union[Device, int] = None) -> int:
    r"""Deprecated; see :func:`~torch.cuda.memory_reserved`."""
    warnings.warn(
        "torch.cuda.memory_cached has been renamed to torch.cuda.memory_reserved",
        FutureWarning)
    return memory_reserved(device=device)
