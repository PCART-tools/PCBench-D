def _join_unicode(lines, sep=''):
    try:
        return sep.join(lines)
    except UnicodeDecodeError:
        sep = compat.text_type(sep)
        return sep.join([x.decode('utf-8') if isinstance(x, str) else x
                         for x in lines])
