def factor_prefix(vals, do_it):
    vals = [format_value(v) for v in vals]
    prefix = commonprefix(vals) if len(vals) > 1 and do_it else ''
    joined = ', '.join(v[len(prefix):] for v in vals)
    return '%s[%s]' % (prefix, joined) if prefix else joined
