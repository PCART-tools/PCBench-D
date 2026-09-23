class maxdict(dict):
    """
    A dictionary with a maximum size.

    Notes
    -----
    This doesn't override all the relevant methods to constrain the size,
    just ``__setitem__``, so use with caution.
    """
    def __init__(self, maxsize):
        dict.__init__(self)
        self.maxsize = maxsize
        self._killkeys = []

    def __setitem__(self, k, v):
        if k not in self:
            if len(self) >= self.maxsize:
                del self[self._killkeys[0]]
                del self._killkeys[0]
            self._killkeys.append(k)
        dict.__setitem__(self, k, v)
