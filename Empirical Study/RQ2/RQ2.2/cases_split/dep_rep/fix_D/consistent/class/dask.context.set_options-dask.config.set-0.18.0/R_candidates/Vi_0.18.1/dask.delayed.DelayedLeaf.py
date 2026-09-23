class DelayedLeaf(Delayed):
    __slots__ = ('_obj', '_key', '_pure', '_nout')

    def __init__(self, obj, key, pure=None, nout=None):
        self._obj = obj
        self._key = key
        self._pure = pure
        self._nout = nout

    @property
    def dask(self):
        return {self._key: self._obj}

    def __call__(self, *args, **kwargs):
        return call_function(self._obj, self._key, args, kwargs,
                             pure=self._pure, nout=self._nout)
