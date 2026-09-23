@functools.lru_cache(maxsize=None)
def make_source_context(*args):
    return SourceContext(*args)
