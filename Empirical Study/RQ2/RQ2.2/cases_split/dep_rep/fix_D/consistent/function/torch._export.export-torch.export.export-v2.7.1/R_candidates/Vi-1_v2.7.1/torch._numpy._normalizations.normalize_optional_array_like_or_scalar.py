def normalize_optional_array_like_or_scalar(x, parm=None):
    if x is None:
        return None
    return normalize_array_like_or_scalar(x, parm)
