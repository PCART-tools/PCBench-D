def ensure_unicode(s):
    """ Turn string or bytes to bytes

    >>> ensure_unicode(u'123')
    u'123'
    >>> ensure_unicode('123')
    u'123'
    >>> ensure_unicode(b'123')
    u'123'
    """
    if isinstance(s, unicode):
        return s
    if hasattr(s, 'decode'):
        return s.decode()
    msg = "Object %s is neither a bytes object nor has an encode method"
    raise TypeError(msg % s)
