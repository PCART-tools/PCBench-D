@functools.cache
def common_constants():
    return {
        # We zero-one specialize shapes, so specialize these constants
        # too
        0,
        1,
    }
