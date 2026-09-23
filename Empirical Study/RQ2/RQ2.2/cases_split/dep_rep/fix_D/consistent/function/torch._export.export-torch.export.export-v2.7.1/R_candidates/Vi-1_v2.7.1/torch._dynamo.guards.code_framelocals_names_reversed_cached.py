@functools.lru_cache(None)
def code_framelocals_names_reversed_cached(code: types.CodeType):
    return list(reversed(code_framelocals_names(code)))
