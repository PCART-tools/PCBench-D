def maybe_normalize(arg, parm):
    """Normalize arg if a normalizer is registered."""
    normalizer = normalizers.get(parm.annotation, None)
    return normalizer(arg, parm) if normalizer else arg
