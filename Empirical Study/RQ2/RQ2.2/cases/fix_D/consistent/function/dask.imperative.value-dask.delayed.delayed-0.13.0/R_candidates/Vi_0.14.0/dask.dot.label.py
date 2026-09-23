def label(x, cache=None):
    """

    >>> label('x')
    'x'

    >>> label(('x', 1))
    "('x', 1)"

    >>> from hashlib import md5
    >>> x = 'x-%s-hello' % md5(b'1234').hexdigest()
    >>> x
    'x-81dc9bdb52d04dc20036dbd8313ed055-hello'

    >>> label(x)
    'x-#-hello'

    >>> from uuid import uuid1
    >>> x = 'x-%s-hello' % uuid1()
    >>> x  # doctest: +SKIP
    'x-4c1a3d7e-0b45-11e6-8334-54ee75105593-hello'

    >>> label(x)
    'x-#-hello'
    """
    s = str(x)
    for pattern in (_HASHPAT, _UUIDPAT):
        m = re.search(pattern, s)
        if m is not None:
            for h in m.groups():
                if cache is not None:
                    n = cache.get(h, len(cache))
                    label = '#{0}'.format(n)
                    # cache will be overwritten destructively
                    cache[h] = n
                else:
                    label = '#'
                s = s.replace(h, label)
    return s
