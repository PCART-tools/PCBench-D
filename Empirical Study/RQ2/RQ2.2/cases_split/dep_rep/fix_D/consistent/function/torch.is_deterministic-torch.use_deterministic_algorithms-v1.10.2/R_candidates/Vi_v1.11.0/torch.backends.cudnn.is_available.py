def is_available():
    r"""Returns a bool indicating if CUDNN is currently available."""
    return torch._C.has_cudnn
