class Item(DaskMethodsMixin):
    def __init__(self, dsk, key):
        self.dask = dsk
        self.key = key
        self.name = key

    def __dask_graph__(self):
        return self.dask

    def __dask_keys__(self):
        return [self.key]

    def __dask_tokenize__(self):
        return self.key

    __dask_optimize__ = globalmethod(optimize, key='bag_optimize',
                                     falsey=dont_optimize)
    __dask_scheduler__ = staticmethod(mpget)

    def __dask_postcompute__(self):
        return finalize_item, ()

    def __dask_postpersist__(self):
        return Item, (self.key,)

    @staticmethod
    def from_delayed(value):
        """ Create bag item from a dask.delayed value.

        See ``dask.bag.from_delayed`` for details
        """
        from dask.delayed import Delayed, delayed
        if not isinstance(value, Delayed) and hasattr(value, 'key'):
            value = delayed(value)
        assert isinstance(value, Delayed)
        return Item(ensure_dict(value.dask), value.key)

    @property
    def _args(self):
        return (self.dask, self.key)

    def __getstate__(self):
        return self._args

    def __setstate__(self, state):
        self.dask, self.key = state

    def apply(self, func):
        name = 'apply-{0}-{1}'.format(funcname(func), tokenize(self, func))
        dsk = {name: (func, self.key)}
        return Item(merge(self.dask, dsk), name)

    __int__ = __float__ = __complex__ = __bool__ = DaskMethodsMixin.compute

    def to_delayed(self, optimize_graph=True):
        """Convert into a ``dask.delayed`` object.

        Parameters
        ----------
        optimize_graph : bool, optional
            If True [default], the graph is optimized before converting into
            ``dask.delayed`` objects.
        """
        from dask.delayed import Delayed
        dsk = self.__dask_graph__()
        if optimize_graph:
            dsk = self.__dask_optimize__(dsk, self.__dask_keys__())
        return Delayed(self.key, dsk)
