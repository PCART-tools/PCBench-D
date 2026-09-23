def _sanitize_str(s):
    if isinstance(s, text_type):
        sanitized = s
    elif isinstance(s, binary_type):
        sanitized = s.decode('ascii', errors='ignore')
    else:
        sanitized = str(s)
    if len(sanitized) < 64:
        return "'%s'" % sanitized
    else:
        return "'%s'" % sanitized[:64] + '...<+len=%d>' % (len(sanitized) - 64)
