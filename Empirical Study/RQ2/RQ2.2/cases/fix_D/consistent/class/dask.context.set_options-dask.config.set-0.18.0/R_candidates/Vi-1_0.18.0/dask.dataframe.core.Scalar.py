class Scalar(DaskMethodsMixin, OperatorMethodMixin):
    """ A Dask object to represent a pandas scalar"""
    def __init__(self, dsk, name, meta, divisions=None):
        # divisions is ignored, only present to be compatible with other
        # objects.
        self.dask = dsk
        self._name = name
        meta = make_meta(meta)
        if isinstance(meta, (pd.DataFrame, pd.Series, pd.Index)):
            raise TypeError("Expected meta to specify scalar, got "
                            "{0}".format(type(meta).__name__))
        self._meta = meta

    def __dask_graph__(self):
        return self.dask

    def __dask_keys__(self):
        return [self.key]

    def __dask_tokenize__(self):
        return self._name

    __dask_optimize__ = globalmethod(optimize, key='dataframe_optimize',
                                     falsey=dont_optimize)
    __dask_scheduler__ = staticmethod(threaded.get)

    def __dask_postcompute__(self):
        return first, ()

    def __dask_postpersist__(self):
        return Scalar, (self._name, self._meta, self.divisions)

    @property
    def _meta_nonempty(self):
        return self._meta

    @property
    def dtype(self):
        return self._meta.dtype

    def __dir__(self):
        o = set(dir(type(self)))
        o.update(self.__dict__)
        if not hasattr(self._meta, 'dtype'):
            o.remove('dtype')  # dtype only in `dir` if available
        return list(o)

    @property
    def divisions(self):
        """Dummy divisions to be compat with Series and DataFrame"""
        return [None, None]

    def __repr__(self):
        name = self._name if len(self._name) < 10 else self._name[:7] + '...'
        if hasattr(self._meta, 'dtype'):
            extra = ', dtype=%s' % self._meta.dtype
        else:
            extra = ', type=%s' % type(self._meta).__name__
        return "dd.Scalar<%s%s>" % (name, extra)

    def __array__(self):
        # array interface is required to support pandas instance + Scalar
        # Otherwise, above op results in pd.Series of Scalar (object dtype)
        return np.asarray(self.compute())

    @property
    def _args(self):
        return (self.dask, self._name, self._meta)

    def __getstate__(self):
        return self._args

    def __setstate__(self, state):
        self.dask, self._name, self._meta = state

    @property
    def key(self):
        return (self._name, 0)

    @classmethod
    def _get_unary_operator(cls, op):
        def f(self):
            name = funcname(op) + '-' + tokenize(self)
            dsk = {(name, 0): (op, (self._name, 0))}
            meta = op(self._meta_nonempty)
            return Scalar(merge(dsk, self.dask), name, meta)
        return f

    @classmethod
    def _get_binary_operator(cls, op, inv=False):
        return lambda self, other: _scalar_binary(op, self, other, inv=inv)

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
