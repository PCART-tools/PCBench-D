def is_initialized():
    r"""Returns whether PyTorch's CUDA state has been initialized."""
    return _initialized and not _is_in_bad_fork()
