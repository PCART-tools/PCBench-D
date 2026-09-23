def _fix_and_maybe_deprecate_out_named_y(f):
    """
    Use the appropriate decorator, depending upon if dispatching is being used.
    """
    if ARRAY_FUNCTION_ENABLED:
        return _fix_out_named_y(f)
    else:
        return _deprecate_out_named_y(f)
