def _get_tensor_sizes(x, allow_nonstatic=True):
    if not _is_tensor(x) or x.type() is None:
        return None
    if allow_nonstatic:
        # Each individual symbol is returned as None.
        # e.g. [1, "a", "b"] -> [1, None, None]
        return x.type().varyingSizes()
    # returns None, if exists any symbol in sizes.
    # e.g. [1, "a", "b"] -> None
    return x.type().sizes()
