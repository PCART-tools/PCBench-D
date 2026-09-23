class da_frompyfunc(object):
    """A serializable `frompyfunc` object"""
    def __init__(self, func, nin, nout):
        self._ufunc = np.frompyfunc(func, nin, nout)
        self._func = func
        self.nin = nin
        self.nout = nout
        self._name = funcname(func)
        self.__name__ = 'frompyfunc-%s' % self._name

    def __repr__(self):
        return 'da.frompyfunc<%s, %d, %d>' % (self._name, self.nin, self.nout)

    def __dask_tokenize__(self):
        return (normalize_function(self._func), self.nin, self.nout)

    def __reduce__(self):
        return (da_frompyfunc, (self._func, self.nin, self.nout))

    def __call__(self, *args, **kwargs):
        return self._ufunc(*args, **kwargs)

    def __getattr__(self, a):
        if not a.startswith('_'):
            return getattr(self._ufunc, a)
        raise AttributeError("%r object has no attribute "
                             "%r" % (type(self).__name__, a))

    def __dir__(self):
        o = set(dir(type(self)))
        o.update(self.__dict__)
        o.update(dir(self._ufunc))
        return list(o)
