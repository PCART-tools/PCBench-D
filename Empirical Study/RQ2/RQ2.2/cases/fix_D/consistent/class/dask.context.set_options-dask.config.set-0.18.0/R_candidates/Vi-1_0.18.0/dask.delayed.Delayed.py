class Delayed(DaskMethodsMixin, OperatorMethodMixin):
    """Represents a value to be computed by dask.

    Equivalent to the output from a single key in a dask graph.
    """
    __slots__ = ('_key', 'dask', '_length')

    def __init__(self, key, dsk, length=None):
        self._key = key
        if type(dsk) is list:  # compatibility with older versions
            dsk = sharedict.merge(*dsk)
        self.dask = dsk
        self._length = length

    def __dask_graph__(self):
        return self.dask

    def __dask_keys__(self):
        return [self.key]

    def __dask_tokenize__(self):
        return self.key

    __dask_scheduler__ = staticmethod(threaded.get)
    __dask_optimize__ = globalmethod(dont_optimize, key='delayed_optimize')

    def __dask_postcompute__(self):
        return single_key, ()

    def __dask_postpersist__(self):
        return rebuild, (self._key, getattr(self, '_length', None))

    def __getstate__(self):
        return tuple(getattr(self, i) for i in self.__slots__)

    def __setstate__(self, state):
        for k, v in zip(self.__slots__, state):
            setattr(self, k, v)

    @property
    def key(self):
        return self._key

    def __repr__(self):
        return "Delayed({0})".format(repr(self.key))

    def __hash__(self):
        return hash(self.key)

    def __dir__(self):
        return dir(type(self))

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError("Attribute {0} not found".format(attr))
        return DelayedAttr(self, attr)

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            object.__setattr__(self, attr, val)
        else:
            raise TypeError("Delayed objects are immutable")

    def __setitem__(self, index, val):
        raise TypeError("Delayed objects are immutable")

    def __iter__(self):
        if getattr(self, '_length', None) is None:
            raise TypeError("Delayed objects of unspecified length are "
                            "not iterable")
        for i in range(self._length):
            yield self[i]

    def __len__(self):
        if getattr(self, '_length', None) is None:
            raise TypeError("Delayed objects of unspecified length have "
                            "no len()")
        return self._length

    def __call__(self, *args, **kwargs):
        pure = kwargs.pop('pure', None)
        name = kwargs.pop('dask_key_name', None)
        func = delayed(apply, pure=pure)
        if name is not None:
            return func(self, args, kwargs, dask_key_name=name)
        return func(self, args, kwargs)

    def __bool__(self):
        raise TypeError("Truth of Delayed objects is not supported")

    __nonzero__ = __bool__

    @classmethod
    def _get_binary_operator(cls, op, inv=False):
        method = delayed(right(op) if inv else op, pure=True)
        return lambda *args, **kwargs: method(*args, **kwargs)

    _get_unary_operator = _get_binary_operator
