def ensure_bytes(s):
    """ Turn string or bytes to bytes

    >>> ensure_bytes(u'123')
    '123'
    >>> ensure_bytes('123')
    '123'
    >>> ensure_bytes(b'123')
    '123'
    """
    if isinstance(s, bytes):
        return s
    if hasattr(s, 'encode'):
        return s.encode()
    msg = "Object %s is neither a bytes object nor has an encode method"
    raise TypeError(msg % s)
