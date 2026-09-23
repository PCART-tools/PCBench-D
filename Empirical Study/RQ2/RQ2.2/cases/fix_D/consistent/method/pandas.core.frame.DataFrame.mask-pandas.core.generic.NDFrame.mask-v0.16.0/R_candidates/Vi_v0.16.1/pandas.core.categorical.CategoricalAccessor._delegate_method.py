    def _delegate_method(self, name, *args, **kwargs):
        from pandas import Series
        method = getattr(self.categorical, name)
        res = method(*args, **kwargs)
        if not res is None:
            return Series(res, index=self.index)
