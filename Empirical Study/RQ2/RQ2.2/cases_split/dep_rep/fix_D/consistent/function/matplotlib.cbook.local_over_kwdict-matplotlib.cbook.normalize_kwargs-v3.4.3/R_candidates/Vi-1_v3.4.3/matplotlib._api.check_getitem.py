def check_getitem(_mapping, **kwargs):
    """
    *kwargs* must consist of a single *key, value* pair.  If *key* is in
    *_mapping*, return ``_mapping[value]``; else, raise an appropriate
    ValueError.

    Examples
    --------
    >>> _api.check_getitem({"foo": "bar"}, arg=arg)
    """
    mapping = _mapping
    if len(kwargs) != 1:
        raise ValueError("check_getitem takes a single keyword argument")
    (k, v), = kwargs.items()
    try:
        return mapping[v]
    except KeyError:
        raise ValueError(
            "{!r} is not a valid value for {}; supported values are {}"
            .format(v, k, ', '.join(map(repr, mapping)))) from None
