class StringAccessor(object):
    """ String processing functions

    Examples
    --------

    >>> import dask.bag as db
    >>> b = db.from_sequence(['Alice Smith', 'Bob Jones', 'Charlie Smith'])
    >>> list(b.str.lower())
    ['alice smith', 'bob jones', 'charlie smith']

    >>> list(b.str.match('*Smith'))
    ['Alice Smith', 'Charlie Smith']

    >>> list(b.str.split(' '))
    [['Alice', 'Smith'], ['Bob', 'Jones'], ['Charlie', 'Smith']]
    """
    def __init__(self, bag):
        self._bag = bag

    def __dir__(self):
        return sorted(set(dir(type(self)) + dir(str)))

    def _strmap(self, key, *args, **kwargs):
        return self._bag.map(lambda s: getattr(s, key)(*args, **kwargs))

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            if key in dir(str):
                func = getattr(str, key)
                return robust_wraps(func)(partial(self._strmap, key))
            else:
                raise

    def match(self, pattern):
        """ Filter strings by those that match a pattern.

        Examples
        --------

        >>> import dask.bag as db
        >>> b = db.from_sequence(['Alice Smith', 'Bob Jones', 'Charlie Smith'])
        >>> list(b.str.match('*Smith'))
        ['Alice Smith', 'Charlie Smith']

        See Also
        --------
        fnmatch.fnmatch
        """
        from fnmatch import fnmatch
        return self._bag.filter(partial(fnmatch, pat=pattern))
