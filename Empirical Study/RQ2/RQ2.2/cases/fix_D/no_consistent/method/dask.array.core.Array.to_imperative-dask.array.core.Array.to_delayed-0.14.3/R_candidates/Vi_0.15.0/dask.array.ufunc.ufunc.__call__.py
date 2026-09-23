    def __call__(self, *args, **kwargs):
        dsk = [arg for arg in args if hasattr(arg, '_elemwise')]
        if len(dsk) > 0:
            return dsk[0]._elemwise(self._ufunc, *args, **kwargs)
        else:
            return self._ufunc(*args, **kwargs)
