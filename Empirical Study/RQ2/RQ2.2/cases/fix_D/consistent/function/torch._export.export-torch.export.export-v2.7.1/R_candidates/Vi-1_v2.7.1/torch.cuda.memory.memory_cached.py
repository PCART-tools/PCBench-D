@deprecated(
    "`torch.cuda.memory_cached` has been renamed to `torch.cuda.memory_reserved`",
    category=FutureWarning,
)
def memory_cached(device: Union[Device, int] = None) -> int:
    r"""Deprecated; see :func:`~torch.cuda.memory_reserved`."""
    return memory_reserved(device=device)
