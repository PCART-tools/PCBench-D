def validate_axisbelow(s):
    try:
        return validate_bool(s)
    except ValueError:
        if isinstance(s, str):
            if s == 'line':
                return 'line'
    raise ValueError('%s cannot be interpreted as'
                     ' True, False, or "line"' % s)
