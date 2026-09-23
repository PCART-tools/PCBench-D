def _ensure_has_len(seq):
    """If seq is an iterator, put its values into a list."""
    try:
        len(seq)
    except TypeError:
        return list(seq)
    else:
        return seq
