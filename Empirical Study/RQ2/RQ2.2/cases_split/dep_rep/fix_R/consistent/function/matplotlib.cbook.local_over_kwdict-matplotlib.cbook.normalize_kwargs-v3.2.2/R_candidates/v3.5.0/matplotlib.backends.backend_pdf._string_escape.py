def _string_escape(match):
    m = match.group(0)
    if m in br'\()':
        return b'\\' + m
    elif m == b'\n':
        return br'\n'
    elif m == b'\r':
        return br'\r'
    assert False
