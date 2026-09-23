    def _delegate_method(self, name, *args, **kwargs):
        """ method delegation to the .values """
        method = getattr(self.values, name)
        if 'inplace' in kwargs:
            raise ValueError("cannot use inplace with CategoricalIndex")
        res = method(*args, **kwargs)
        if lib.isscalar(res):
            return res
        return CategoricalIndex(res, name=self.name)
