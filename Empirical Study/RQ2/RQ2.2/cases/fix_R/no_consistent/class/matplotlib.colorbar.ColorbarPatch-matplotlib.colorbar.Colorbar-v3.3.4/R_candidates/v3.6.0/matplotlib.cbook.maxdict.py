@_api.deprecated("3.6", alternative="functools.lru_cache")
class maxdict(dict):
    """
    A dictionary with a maximum size.

    Notes
    -----
    This doesn't override all the relevant methods to constrain the size,
    just ``__setitem__``, so use with caution.
    """

    def __init__(self, maxsize):
        super().__init__()
        self.maxsize = maxsize

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        while len(self) >= self.maxsize:
            del self[next(iter(self))]
