class Tuple(DaskMethodsMixin):
    __slots__ = ('_dask', '_keys')
    __dask_scheduler__ = staticmethod(dask.threaded.get)

    def __init__(self, dsk, keys):
        self._dask = dsk
        self._keys = keys

    def __add__(self, other):
        if isinstance(other, Tuple):
            return Tuple(merge(self._dask, other._dask),
                         self._keys + other._keys)
        return NotImplemented

    def __dask_graph__(self):
        return self._dask

    def __dask_keys__(self):
        return self._keys

    def __dask_tokenize__(self):
        return self._keys

    def __dask_postcompute__(self):
        return tuple, ()

    def __dask_postpersist__(self):
        return Tuple, (self._keys,)
