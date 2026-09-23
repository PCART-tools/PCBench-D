@_api.deprecated("3.3")
def validate_bool_maybe_none(b):
    """Convert b to ``bool`` or raise, passing through *None*."""
    if isinstance(b, str):
        b = b.lower()
    if b is None or b == 'none':
        return None
    if b in ('t', 'y', 'yes', 'on', 'true', '1', 1, True):
        return True
    elif b in ('f', 'n', 'no', 'off', 'false', '0', 0, False):
        return False
    else:
        raise ValueError('Could not convert "%s" to bool' % b)
