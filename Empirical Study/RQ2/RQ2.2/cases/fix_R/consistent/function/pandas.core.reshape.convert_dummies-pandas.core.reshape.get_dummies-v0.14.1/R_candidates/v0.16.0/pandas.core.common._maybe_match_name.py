def _maybe_match_name(a, b):
    a_name = getattr(a, 'name', None)
    b_name = getattr(b, 'name', None)
    if a_name == b_name:
        return a_name
    return None
