def _maybe_match_name(a, b):
    a_has = hasattr(a, 'name')
    b_has = hasattr(b, 'name')
    if a_has and b_has:
        if a.name == b.name:
            return a.name
        else:
            return None
    elif a_has:
        return a.name
    elif b_has:
        return b.name
    return None
