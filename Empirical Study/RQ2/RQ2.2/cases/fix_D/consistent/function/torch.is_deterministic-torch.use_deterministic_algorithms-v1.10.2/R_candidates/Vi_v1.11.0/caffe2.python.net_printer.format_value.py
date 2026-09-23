def format_value(val):
    if isinstance(val, list):
        return '[%s]' % ', '.join("'%s'" % str(v) for v in val)
    else:
        return str(val)
