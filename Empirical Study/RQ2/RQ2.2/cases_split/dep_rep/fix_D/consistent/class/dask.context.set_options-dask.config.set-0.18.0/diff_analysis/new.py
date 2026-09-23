class set(object):
    """ Temporarily set configuration values within a context manager

    Examples
    --------
    >>> import dask
    >>> with dask.config.set({'foo': 123}):
    ...     pass

    See Also
    --------
    dask.config.get
    """
    def __init__(self, arg=None, config=config, lock=config_lock, **kwargs):
        if arg and not kwargs:
            kwargs = arg

        with lock:
            self.config = config
            self.old = {}

            for key, value in kwargs.items():
                self._assign(key.split('.'), value, config, old=self.old)

    def __enter__(self):
        return self.config

    def __exit__(self, type, value, traceback):
        for keys, value in self.old.items():
            if value == '--delete--':
                d = self.config
                try:
                    while len(keys) > 1:
                        d = d[keys[0]]
                        keys = keys[1:]
                    del d[keys[0]]
                except KeyError:
                    pass
            else:
                self._assign(keys, value, self.config)

    @classmethod
    def _assign(cls, keys, value, d, old=None, path=[]):
        """ Assign value into a nested configuration dictionary

        Optionally record the old values in old

        Parameters
        ----------
        keys: Sequence[str]
            The nested path of keys to assign the value, similar to toolz.put_in
        value: object
        d: dict
            The part of the nested dictionary into which we want to assign the
            value
        old: dict, optional
            If provided this will hold the old values
        path: List[str]
            Used internally to hold the path of old values
        """
        if len(keys) == 1:
            if old is not None:
                path_key = tuple(path + [keys[0]])
                if keys[0] in d:
                    old[path_key] = d[keys[0]]
                else:
                    old[path_key] = '--delete--'
            d[keys[0]] = value
        else:
            key = keys[0]
            if key not in d:
                d[key] = {}
                if old is not None:
                    old[tuple(path + [key])] = '--delete--'
                old = None
            cls._assign(keys[1:], value, d[key], path=path + [key], old=old)
