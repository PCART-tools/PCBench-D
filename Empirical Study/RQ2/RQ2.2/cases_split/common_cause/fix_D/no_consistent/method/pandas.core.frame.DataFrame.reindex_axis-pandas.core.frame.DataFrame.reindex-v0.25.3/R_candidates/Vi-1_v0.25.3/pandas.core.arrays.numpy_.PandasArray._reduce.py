    def _reduce(self, name, skipna=True, **kwargs):
        meth = getattr(self, name, None)
        if meth:
            return meth(skipna=skipna, **kwargs)
        else:
            msg = "'{}' does not implement reduction '{}'"
            raise TypeError(msg.format(type(self).__name__, name))
