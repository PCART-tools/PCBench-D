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
            self.old = copy.deepcopy(config)

            def assign(keys, value, d):
                key = keys[0]
                if len(keys) == 1:
                    d[keys[0]] = value
                else:
                    if key not in d:
                        d[key] = {}
                    assign(keys[1:], value, d[key])

            for key, value in kwargs.items():
                assign(key.split('.'), value, config)

    def __enter__(self):
        return config

    def __exit__(self, type, value, traceback):
        self.config.clear()
        self.config.update(self.old)
