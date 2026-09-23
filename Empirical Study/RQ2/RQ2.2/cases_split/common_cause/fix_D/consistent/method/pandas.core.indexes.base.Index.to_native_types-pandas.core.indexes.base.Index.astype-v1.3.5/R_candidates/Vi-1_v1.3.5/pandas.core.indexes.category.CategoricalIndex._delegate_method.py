    def _delegate_method(self, name: str, *args, **kwargs):
        """method delegation to the ._values"""
        method = getattr(self._values, name)
        if "inplace" in kwargs:
            raise ValueError("cannot use inplace with CategoricalIndex")
        res = method(*args, **kwargs)
        if is_scalar(res):
            return res
        return CategoricalIndex(res, name=self.name)
