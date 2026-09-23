@contextlib.contextmanager
def vmap_increment_nesting(batch_size, randomness):
    try:
        vmap_level = _vmap_increment_nesting(batch_size, randomness)
        yield vmap_level
    finally:
        _vmap_decrement_nesting()
