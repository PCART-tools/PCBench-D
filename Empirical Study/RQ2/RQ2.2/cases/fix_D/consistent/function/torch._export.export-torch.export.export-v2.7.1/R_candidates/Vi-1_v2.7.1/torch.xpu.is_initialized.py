def is_initialized():
    r"""Return whether PyTorch's XPU state has been initialized."""
    return _initialized and not _is_in_bad_fork()
