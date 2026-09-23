@deprecated(
    "`torch.cuda.max_memory_cached` has been renamed to `torch.cuda.max_memory_reserved`",
    category=FutureWarning,
)
def max_memory_cached(device: "Device" = None) -> int:
    r"""Deprecated; see :func:`~torch.cuda.max_memory_reserved`."""
    return max_memory_reserved(device=device)
