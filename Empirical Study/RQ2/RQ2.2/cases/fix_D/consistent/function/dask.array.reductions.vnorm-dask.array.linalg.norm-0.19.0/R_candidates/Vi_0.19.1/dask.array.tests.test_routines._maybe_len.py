def _maybe_len(l):
    try:
        return len(l)
    except TypeError:
        return 0
