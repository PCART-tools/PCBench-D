def validate_sketch(s):
    if isinstance(s, str):
        s = s.lower()
    if s == 'none' or s is None:
        return None
    try:
        return tuple(_listify_validator(validate_float, n=3)(s))
    except ValueError:
        raise ValueError("Expected a (scale, length, randomness) triplet")
