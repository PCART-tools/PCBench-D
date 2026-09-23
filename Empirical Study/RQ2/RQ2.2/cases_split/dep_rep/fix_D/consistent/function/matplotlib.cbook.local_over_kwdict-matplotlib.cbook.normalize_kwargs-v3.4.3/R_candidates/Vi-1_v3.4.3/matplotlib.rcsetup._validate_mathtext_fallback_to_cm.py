def _validate_mathtext_fallback_to_cm(b):
    """
    Temporary validate for fallback_to_cm, while deprecated

    """
    if isinstance(b, str):
        b = b.lower()
    if b is None or b == 'none':
        return None
    else:
        _api.warn_deprecated(
            "3.3", message="Support for setting the 'mathtext.fallback_to_cm' "
            "rcParam is deprecated since %(since)s and will be removed "
            "%(removal)s; use 'mathtext.fallback : 'cm' instead.")
        return validate_bool_maybe_none(b)
