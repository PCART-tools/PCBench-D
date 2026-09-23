def is_available():
    r"""Return a bool indicating if CUDNN is currently available."""
    return torch._C._has_cudnn
