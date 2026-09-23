@contextmanager
def flags(enabled=False):
    r"""Context manager for setting if nnpack is enabled globally"""
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(enabled)
    try:
        yield
    finally:
        with __allow_nonbracketed_mutation():
            set_flags(orig_flags[0])
