class Tuple(object):
    __dask_scheduler__ = staticmethod(dask.threaded.get)

    def __init__(self, dsk, keys):
        self._dask = dsk
        self._keys = keys

    def __dask_tokenize__(self):
        return self._keys

    def __dask_graph__(self):
        return self._dask

    def __dask_keys__(self):
        return self._keys

    def __dask_postcompute__(self):
        return tuple, ()
