@contextmanager
def flags(enabled=False, deterministic=False, allow_tf32=True):
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(enabled, deterministic, allow_tf32)
    try:
        yield
    finally:
        with __allow_nonbracketed_mutation():
            set_flags(*orig_flags)
