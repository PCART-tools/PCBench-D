    def _reduce(self, name, skipna=True, **kwargs):
        meth = getattr(self, name, None)
        if meth:
            return meth(skipna=skipna, **kwargs)
        else:
            msg = f"'{type(self).__name__}' does not implement reduction '{name}'"
            raise TypeError(msg)
