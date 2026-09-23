def is_available():
    return hasattr(torch._C, "_dist_autograd_init")
