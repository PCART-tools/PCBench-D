def _escape_val(val, escape_func):
    """
    Given a string value or a list of string values, run each value through
    the input escape function to make the values into legal font config
    strings.  The result is returned as a string.
    """
    if not np.iterable(val) or isinstance(val, str):
        val = [val]

    return ','.join(escape_func(r'\\\1', str(x)) for x in val
                    if x is not None)
